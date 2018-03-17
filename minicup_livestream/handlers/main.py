# coding=utf-8
import tornado.web

from minicup_administration.core.models import Match


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('match.html')