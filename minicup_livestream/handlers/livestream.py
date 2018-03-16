# coding=utf-8
import logging

import tornado.escape
import tornado.websocket


class LiveStreamHandler(tornado.websocket.WebSocketHandler):
    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        self.write_message("")

    def on_close(self):
        pass

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)