# coding=utf-8
import tornado.web

from core.models import Category


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        for c in Category.objects.all():
            self.write("Hello world {}!<br />".format(c))