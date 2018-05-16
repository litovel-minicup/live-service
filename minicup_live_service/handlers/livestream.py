# coding=utf-8
import datetime
import logging
from collections import defaultdict
from typing import DefaultDict, Set, Union, Type
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.timezone import now
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from minicup_live_service.handlers.base import ApplicationStartHandlerMixin
from minicup_model.core.models import Match, MatchEvent, Player, TeamInfo
from ..service.match_event import MatchEventMessageGenerator

logger = logging.getLogger(__name__)


class PermissionDenied(Exception):
    pass


def check_user(fc):
    def _(self: "LivestreamHandler", *args, **kwargs):
        if not self.get_secure_cookie('user'):
            raise PermissionDenied()
        return fc(self, *args, **kwargs)

    return _


class LivestreamHandler(ApplicationStartHandlerMixin, WebSocketHandler):
    # enable compression
    get_compression_options = lambda self: {}

    subscribers = defaultdict(set)  # type: DefaultDict[int, Set[WebSocketHandler]]

    match_event_message_generator = MatchEventMessageGenerator()

    def check_origin(self, origin):
        loc = urlparse(origin).netloc  # type: str
        return loc in settings.WS_ALLOWED_ORIGINS or loc.startswith('localhost') or loc.startswith('127.')

    def on_pong(self, data):
        pass

    def open(self, *args, **kwargs):
        logger.debug('OPEN: {}'.format(self))
        self.set_nodelay(True)
        if self.get_secure_cookie('user'):
            self.write_message(dict(
                logged=True
            ))

    def on_close(self):
        logger.debug('CLOSE: {}'.format(self))
        self.unsubscribe(self)

    @transaction.atomic
    def on_message(self, message):
        try:
            data = json_decode(message)
        except ValueError as e:
            self.write_message(dict(
                success=False,
                message=str(e)
            ))
            return

        logger.debug("Message: %r", data)
        try:
            self._process_message(data)
        except ObjectDoesNotExist as e:
            self.write_message(dict(
                success=False,
                message=str(e)
            ))
        except PermissionDenied as e:
            self.write_message(dict(
                success=False,
                message='Not enough perms to perform action.'
            ))

    def _process_message(self, data: dict):
        logger.info('{}: {}'.format(data.get('action', '').upper(), data))
        if data.get('action') == 'goal':
            self.subscribe_from_data(data=data)
            self._process_goal(data)

        elif data.get('action') == 'state_change':
            self.subscribe_from_data(data=data)
            self._process_state_change(data)

        elif data.get('action') == 'delete_event':
            self.subscribe_from_data(data=data)
            self._delete_event(data)

        elif data.get('action') == 'subscribe':
            self.subscribe_from_data(data=data)
            match = Match.objects.get(pk=data.get('match'))

            self.write_message(dict(match=match.serialize()))
        else:
            self.write_message(dict(
                success=False,
                message='Unknown action {}.'.format(data.get('action'))
            ))

    def subscribe_from_data(self, data):
        match = Match.objects.get(pk=data.get('match'))
        self.subscribe(match=match, subscriber=self)

    @check_user
    def _process_goal(self, data):
        match = Match.objects.get(pk=data.get('match'))
        team_info = TeamInfo.objects.get(pk=data.get('team'))

        try:
            player = Player.objects.get(pk=data.get('player'))
        except Player.DoesNotExist:
            player = None

        rivals = (match.home_team_info, match.away_team_info)
        if player and player.team_info != team_info:
            # TODO: problem
            logger.error('Player {} cannot score for team match {}.'.format(player, team_info))
            pass

        scores = [match.score_home or 0, match.score_away or 0]
        scores[rivals.index(team_info)] += 1
        # type: datetime
        starts = (match.first_half_start, match.second_half_start)
        half_start = max(filter(None, starts))

        # type: MatchEvent
        match_event = MatchEvent(
            match=match,
            player=player,
            team_info=team_info,
            type=MatchEvent.TYPE_GOAL,
            score_home=scores[0],
            score_away=scores[1],
            # not longer then half length
            time_offset=min((int((now() - half_start).total_seconds()), Match.HALF_LENGTH.total_seconds())),
            half_index=starts.index(half_start)
        )
        match_event.message = self.match_event_message_generator.generate(match_event=match_event)
        match_event.save()
        match.score_home, match.score_away = scores
        match.save()
        self.notify(match, dict(
            event=match_event.serialize(),
            match=match.serialize(),
        ))

    @check_user
    def _process_state_change(self, data):
        match = Match.objects.get(pk=data.get('match'))
        state = data.get('state')

        event = match.change_state(state)
        if not event:
            return

        if state == Match.STATE_HALF_FIRST:
            match.first_half_start = now()
            IOLoop.current().call_later(Match.HALF_LENGTH.total_seconds(), self._on_timer_end(match=match))

        elif state == Match.STATE_HALF_SECOND:
            match.second_half_start = now()
            IOLoop.current().call_later(Match.HALF_LENGTH.total_seconds(), self._on_timer_end(match=match))

        match.save(update_fields=('first_half_start', 'second_half_start',))

        data = dict(match=match.serialize(), event=event.serialize() if event else None)
        self.notify(match, {k: v for k, v in data.items() if v})

    @classmethod
    def on_application_start(cls, _: Application):
        """
        For all matches with required timer end plans callbacks to end half.
        """
        io_loop = IOLoop.current()
        for match in Match.objects.find_matches_with_required_timer():  # type: Match
            timer_end = ((match.second_half_start or match.first_half_start) + Match.HALF_LENGTH).timestamp()
            logging.info('MATCH {}: Planning timer end in {}.'.format(match.id, timer_end - io_loop.time()))
            io_loop.call_at(
                timer_end,
                cls._on_timer_end(match=match)
            )

    @classmethod
    def _on_timer_end(cls, match: Match):
        def cb(handler: Type[LivestreamHandler] = cls):
            event = match.on_timer_end()
            data = dict(match=match.serialize(), event=event.serialize() if event else None)
            handler.notify(match, {k: v for k, v in data.items() if v})

        return cb

    @check_user
    def _delete_event(self, data):
        event = MatchEvent.objects.get(pk=data.get('event'))  # type: MatchEvent
        match = event.match
        logger.info('Deleting {}.'.format(event))
        before = match.match_match_event.exclude(pk=event.pk).last()  # type: MatchEvent

        if before:
            match.score_home, match.score_away = before.score
        else:
            match.score_home, match.score_away = 0, 0

        if match.confirmed:
            # TODO: old events cannot be deleted
            self.write_message(dict(
                match=match.serialize(),
                success=False,
            ))
            return

        event.delete()
        match.save(update_fields=('score_home', 'score_away'))

        self.notify(match, dict(
            match=match.serialize(),
            events=[
                e.serialize() for e in match.match_match_event.all()
            ]
        ))

    @classmethod
    def notify(cls, match: Match, message: Union[dict, str]):
        logger.info('NOTIFY: {} subs, {}: {}'.format(
            len(cls.subscribers[match.id]),
            message.get('match', {}).get('id') or message.get('event', {}).get('id'),
            str(message)[:50]
        ))
        for sub in cls.subscribers[match.id]:  # type: WebSocketHandler
            sub.write_message(message)

    @classmethod
    def unsubscribe(cls, subscriber: WebSocketHandler, match: Match = None):
        if match and subscriber in cls.subscribers[match]:
            cls.subscribers[match.id].remove(subscriber)
            return
        for m in cls.subscribers.values():
            if subscriber in m:
                m.remove(subscriber)

    @classmethod
    def subscribe(cls, match: Match, subscriber: WebSocketHandler):
        cls.subscribers[match.id].add(subscriber)

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            dict(self.request.headers).get('User-Agent'),
        )
