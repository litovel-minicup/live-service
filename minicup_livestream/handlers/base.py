# coding=utf-8
from json import dumps

from tornado.websocket import WebSocketHandler


class BaseWebsocketJsonHandler(WebSocketHandler):
    def write_json(self, data):
        self.write_message(dumps(data))
