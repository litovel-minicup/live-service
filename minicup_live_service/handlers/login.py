# coding=utf-8
from minicup_model.core.models import User
from .base import BaseHandler


class LoginHandler(BaseHandler):
    COOKIE_USER = 'user'
    MIN_PIN_LENGTH = 4

    def post(self):
        pin = self.arguments_json.get('pin') or ''

        if len(pin) < self.MIN_PIN_LENGTH or not User.objects.filter(pin=pin).exists():
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
