#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

import logging
import os.path

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from django.conf import settings as django_settings
from tornado.options import define, options

from minicup import settings

define("port", default=8888, help="run on the given port", type=int)

import django

django_settings.configure(settings)

if django.VERSION[:2] > (1, 5):
    django.setup()

from core.models import Category


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super().__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world {}!".format(Category.objects.all()))


class ChatSocketHandler(tornado.websocket.WebSocketHandler):

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


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
