# coding=utf-8
import os.path

import tornado.web

from .handlers import MatchLiveStreamHandler, MainHandler


class Application(tornado.web.Application):
    handlers = [
        (r'/', MainHandler),

        (r'/ws/match-live/(\d+)', MatchLiveStreamHandler),
    ]

    def __init__(self):
        settings_ = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super().__init__(self.handlers, **settings_)
