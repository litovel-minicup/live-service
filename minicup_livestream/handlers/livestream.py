# coding=utf-8
import datetime
import logging
from collections import defaultdict
from typing import DefaultDict, Set, Union

from django.db import transaction
from django.utils.timezone import now
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from minicup_administration.core.models import Match, MatchEvent, Player
from minicup_livestream.service.match_event import MatchEventMessageGenerator


class BroadcastHandler(WebSocketHandler):
    subscribers = defaultdict(set)  # type: DefaultDict[int, Set[WebSocketHandler]]

    match_event_message_generator = MatchEventMessageGenerator()

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def on_pong(self, data):
        pass

    def open(self, *args, **kwargs):
        logging.info('OPEN: ')

    def on_close(self):
        logging.info('CLOSE: ')
        self.unsubscribe(self)

    @transaction.atomic
    def on_message(self, message):
        logging.info("got message %r", message)
        data = json_decode(message)

        logging.info(data.get('action', '').upper())
        if data.get('action') == 'goal':
            self._process_goal(data)
        elif data.get('action') == 'state_change':
            self._process_state_change(data)
        elif data.get('action') == 'subscribe':
            self.subscribe(Match.objects.get(pk=data.get('match')), self)
            logging.info(data)

    def _process_goal(self, data):
        match = Match.objects.get(pk=data.get('match'))
        player = Player.objects.get(pk=data.get('player'))
        rivals = (match.home_team_info, match.away_team_info)
        if player.team_info not in rivals:
            # TODO: problem
            logging.error('Player {} cannot score in match {}.'.format(player, match))
            pass
        scores = [match.score_home, match.score_away]
        scores[rivals.index(player.team_info)] += 1
        # type: datetime
        starts = (match.first_half_start, match.second_half_start)
        half_start = max(filter(None, starts))
        self.subscribe(match=match, subscriber=self)

        # type: MatchEvent
        match_event = MatchEvent.objects.create(
            match=match,
            player=player,
            team_info=player.team_info,
            type=MatchEvent.TYPE_GOAL,
            score_home=scores[0],
            score_away=scores[1],
            time_offset=int((now() - half_start).total_seconds()),
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

    @classmethod
    def notify(cls, match: Match, message: Union[dict, str]):
        for sub in cls.subscribers[match.id]:  # type: WebSocketHandler
            sub.write_message(message)
            logging.info('NOTIFY: {} - {}'.format(sub, str(message)[:50]))

    @classmethod
    def unsubscribe(cls, subscriber: WebSocketHandler, match: Match = None):
        if match and subscriber in cls.subscribers[match]:
            cls.subscribers[match].remove(subscriber)
            return
        for m in cls.subscribers.values():
            if subscriber in m:
                m.remove(subscriber)

    @classmethod
    def subscribe(cls, match: Match, subscriber: WebSocketHandler):
        cls.subscribers[match.id].add(subscriber)

    def _process_state_change(self, data):
        match = Match.objects.get(pk=data.get('match'))
        state = data.get('state')

        if not match.change_state(state):
            return

        if state == Match.STATE_HALF_FIRST:
            match.first_half_start = now()
            IOLoop.current().call_later(Match.HALF_LENGTH.total_seconds(), self._half_end_callback(match_=match))

        elif state == Match.STATE_HALF_SECOND:
            match.second_half_start = now()
            IOLoop.current().call_later(Match.HALF_LENGTH.total_seconds(), self._half_end_callback(match_=match))

        match.save(update_fields=('first_half_start', 'second_half_start', ))
        self.notify(match, dict(
            match=match.serialize()
        ))

    def _half_end_callback(self, match_: Match):
        def cb(handler: BroadcastHandler = self, match: Match = match_):
            match.refresh_from_db(fields=('online_state',))

            if match.online_state == Match.STATE_HALF_FIRST:
                match.change_state(Match.STATE_HALF_PAUSE)
            elif match.online_state == Match.STATE_HALF_SECOND:
                match.change_state(Match.STATE_END)

            handler.notify(match, dict(
                match=match.serialize()
            ))

        return cb

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            dict(self.request.headers).get('User-Agent'),
        )
