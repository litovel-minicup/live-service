# coding=utf-8
import tornado.web
from django.conf import settings


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', v=settings.SERVER_STARTED.timestamp() if not settings.DEBUG else '')
