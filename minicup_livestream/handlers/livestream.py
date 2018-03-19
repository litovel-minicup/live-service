# coding=utf-8
import datetime
import logging
from collections import defaultdict
from typing import DefaultDict, Set, Union

from django.utils.timezone import now
from tornado.escape import json_decode
from tornado.websocket import WebSocketHandler

from minicup_administration.core.models import Match, MatchEvent, Player


class BroadcastHandler(WebSocketHandler):
    subscribers = defaultdict(set)  # type: DefaultDict[int, Set[WebSocketHandler]]

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

    def on_message(self, message):
        logging.info("got message %r", message)
        data = json_decode(message)

        logging.info(data.get('action', '').upper())
        if data.get('action') == 'goal':
            self._process_goal(data)
        elif data.get('action') == 'subscribe':
            self.subscribe(Match.objects.get(pk=data.get('match')), self)
        elif data.get('action') == 'start':
            self._process_start(data)
        else:
            logging.info(data)

    def _process_goal(self, data):
        match = Match.objects.get(pk=data.get('match'))
        player = Player.objects.get(pk=data.get('player'))
        rivals = (match.home_team_info, match.away_team_info)
        if player.team_info not in rivals:
            # TODO: problem
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
            message='New goal from {} - new state is {}.'.format(player, ':'.join(map(str, scores))),
            type=MatchEvent.TYPE_GOAL,
            score_home=scores[0],
            score_away=scores[1],
            time_offset=int((now() - half_start).total_seconds()),
            half_index=starts.index(half_start)
        )
        match.score_home, match.score_away = scores
        match.save()
        self.notify(match, dict(
            event=match_event.serialize(),
            match=match.serialize(),
        ))

    @classmethod
    def notify(cls, match: Match, message: Union[dict, str]):
        for sub in cls.subscribers.get(match.id):  # type: WebSocketHandler
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

    def _process_start(self, data):
        match = Match.objects.get(pk=data.get('match'))

        if match.second_half_start:
            return # TODO: error
        if match.first_half_start:
            match.second_half_start = now()
        else:
            match.first_half_start = now()

        match.save()