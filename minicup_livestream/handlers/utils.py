# coding=utf-8
from tornado.web import RequestHandler, HTTPError


def login_required(method):
    def _(self: RequestHandler, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)

    return _
