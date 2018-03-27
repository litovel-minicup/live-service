# coding=utf-8
import os.path
from os.path import dirname

import tornado.web

from minicup_livestream.handlers.api import CategoryListHandler, MatchListHandler, MatchHandler, MatchEventsHandler
from minicup_livestream.handlers.login import LoginHandler
from .handlers import LivestreamHandler, MainHandler


class Application(tornado.web.Application):
    handlers = [
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(dirname(__file__), 'static')}),

        (r'/ws/broadcast', LivestreamHandler),

        (r'/api/category-list', CategoryListHandler),
        (r'/api/category/(\d+)', MatchListHandler),
        (r'/api/match/(\d+)', MatchHandler),
        (r'/api/match-events/(\d+)', MatchEventsHandler),

        (r'/api/login', LoginHandler),

        (r'/', MainHandler),
    ]

    def __init__(self):
        settings_ = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            websocket_ping_interval=1,
            debug=True,
        )
        super().__init__(self.handlers, **settings_)
