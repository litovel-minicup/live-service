# coding=utf-8
import logging
from json import loads

from tornado.websocket import WebSocketHandler

from minicup_administration.core.models import Player, Match

class BroadcastHandler(WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self, *args, **kwargs):
        logging.info('OPEN:')

    def on_close(self):
        logging.info('CLOSE:')

    def on_message(self, message):
        logging.info("got message %r", message)

        data = loads(message)  # type: dict
        if data.get('action') == 'roster':
            self.write_message(dict(roster=[
                dict(
                    id=p.id,
                    name=p.name,
                    surname=p.surname,
                    number=p.number
                ) for p in Player.objects.filter(team_info_id=data.get('team_info_id'))
            ]))
            return

        if data.get('action') == 'matches':
            self.write_message(dict(matches=[
                dict(
                    id=p.id,
                    name=str(p)
                ) for p in Match.objects.filter(category_id=data.get('category_id'))
            ]))
            return


        self.write_message(dict(success=True, **loads(message)))
