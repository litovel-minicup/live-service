# coding=utf-8
import tornado.web

from minicup_administration.core.models import Match


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class MatchHandler(tornado.web.RequestHandler):
    def get(self, match_id):
        self.render('match.html', match=Match.objects.get(pk=match_id))
