# coding=utf-8
import logging

from tornado.ioloop import PeriodicCallback

from minicup_administration.core.models import Match
from .base import BaseWebsocketJsonHandler


class MatchLiveStreamHandler(BaseWebsocketJsonHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        self._status_controller = PeriodicCallback(self.ping_data, 2000.)
        self._status_controller.start()

        self._match_id = None

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self, match_id, *args, **kwargs):
        self._match_id = match_id
        match = Match.objects.get(pk=self._match_id)
        logging.info('Params: {}'.format(match))

        self.write_json(dict(
            match_id=match.id,
            home_team_id=match.home_team_info_id,
            home_team_name=match.home_team_info.name,
            away_team_id=match.away_team_info_id,
            away_team_name=match.away_team_info.name,
        ))

    def on_close(self):
        pass

    def on_message(self, message):
        logging.info("got message %r", message)
        self.write_json(dict(success=True))

    def on_pong(self, data):
        logging.info("pong %r", data)

    def ping_data(self):
        self.ping(bytes(str(self._match_id), encoding='utf-8'))
