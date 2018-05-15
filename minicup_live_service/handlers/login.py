# coding=utf-8

from .base import BaseHandler


class LoginHandler(BaseHandler):
    COOKIE_USER = 'user'

    def post(self):
        pin = self.arguments_json.get('pin')

        if not pin or pin not in ('1234',):
            self.write(dict(
                success=False
            ))
            return

        self.set_secure_cookie(self.COOKIE_USER, 'joe')
        self.write(dict(
            success=True
        ))


class LogoutHandler(BaseHandler):
    def post(self):
        self.clear_cookie(LoginHandler.COOKIE_USER)
        self.write(dict(
            success=True
        ))
