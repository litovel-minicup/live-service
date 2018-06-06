# coding=utf-8
import json
import logging
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from django.conf import settings
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler

from minicup_live_service.service.live import LiveService
from .utils import login_required


logger = logging.getLogger(__name__)

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


class BaseWebsocketHandler(WebSocketHandler):
    # enable compression
    get_compression_options = lambda self: {}

    def write_message(self, message, *args, **kwargs):
        if isinstance(message, dict):
            message['server_time'] = datetime.now().timestamp()
            message.setdefault('type_content', []).append(LiveService.MESSAGE_CONTENT_SERVER_TIME)

        return super().write_message(message, *args, **kwargs)

    def check_origin(self, origin):
        loc = urlparse(origin).netloc  # type: str
        is_ok = (
                loc in settings.WS_ALLOWED_ORIGINS or
                loc.startswith('localhost') or
                loc.startswith('127.') or
                loc.startswith('192.') or
                loc.startswith('10.')
        )
        if not is_ok:
            logger.info('Location {} is not OK.'.format(loc))
        return is_ok