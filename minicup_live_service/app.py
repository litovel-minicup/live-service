# coding=utf-8
import os.path
from datetime import timedelta
from os.path import dirname

import tornado.web
from django.conf import settings
from raven.contrib.tornado import SentryMixin, AsyncSentryClient
from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line, options, define

from minicup_live_service.handlers.api import CategoryListHandler, MatchListHandler, MatchHandler, MatchEventsHandler
from minicup_live_service.handlers.base import BaseHandler, ApplicationStartHandlerMixin
from minicup_live_service.handlers.login import LoginHandler, LogoutHandler
from .handlers import LiveStreamHandler, MainHandler

if settings.SENTRY_DSN:
    BaseHandler.__bases__ = (SentryMixin,) + BaseHandler.__bases__


class Application(tornado.web.Application):
    handlers = [
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(dirname(__file__), 'static')}),

        (r'/ws/live', LiveStreamHandler),

        (r'/api/category-list', CategoryListHandler),
        (r'/api/category/(\d+)', MatchListHandler),
        (r'/api/match/(\d+)', MatchHandler),
        (r'/api/match-events/(\d+)', MatchEventsHandler),

        (r'/api/login', LoginHandler),
        (r'/api/logout', LogoutHandler),

        (r'/', MainHandler),
    ]

    def __init__(self):
        settings_ = dict(
            cookie_secret=settings.SECRET_KEY,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            websocket_ping_interval=1,
            debug=os.environ.get("TORNADO_DEBUG") == '1',
        )
        super().__init__(self.handlers, **settings_)

    def listen(self, *args, **kwargs):
        for rule in self.wildcard_router.rules:
            if issubclass(rule.target, ApplicationStartHandlerMixin):
                rule.target.on_application_start(self)

        super(Application, self).listen(*args, **kwargs)


app = Application()

if settings.SENTRY_DSN:
    app.sentry_client = AsyncSentryClient(settings.SENTRY_DSN)


def main():
    define("port", default=8888, help="run on the given port", type=int)

    autoreload.start()

    parse_command_line()
    app.listen(options.port)

    IOLoop.current().start()
