# coding=utf-8
import tornado.web
from django.conf import settings


class MatchOnlineHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('match_online.html', v=settings.SERVER_STARTED.timestamp() if not settings.DEBUG else '')


class MatchOverviewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('match_overview.html', v=settings.SERVER_STARTED.timestamp() if not settings.DEBUG else '')
