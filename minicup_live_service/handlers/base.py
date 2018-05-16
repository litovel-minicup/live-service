# coding=utf-8
import json
from typing import Optional

from tornado.web import RequestHandler, Application

from .utils import login_required


class ApplicationStartHandlerMixin(object):
    @classmethod
    def on_application_start(cls, application: Application):
        pass


class BaseHandler(RequestHandler):
    arguments_json = None  # type: Optional[dict]

    def prepare(self):
        if self.request.headers["Content-Type"].startswith("application/json"):
            self.arguments_json = json.loads(self.request.body.decode('utf-8') or '{}')


class AuthenticatedBaseHandler(BaseHandler):
    COOKIE_USER = 'user'

    def get_current_user(self):
        return self.get_secure_cookie(self.COOKIE_USER)

    @login_required
    def prepare(self):
        pass
