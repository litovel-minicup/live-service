# coding=utf-8
import logging
from collections import defaultdict
from typing import DefaultDict, Set, Union
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from tornado.escape import json_decode
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from minicup_live_service.exceptions import EventDeleteError
from minicup_live_service.handlers.base import ApplicationStartHandlerMixin
from minicup_live_service.service.live import LiveService
from minicup_model.core.models import Match

logger = logging.getLogger(__name__)


class PermissionDenied(Exception):
    pass


def check_user(fc):
    def _(self: "LiveStreamHandler", *args, **kwargs):
        if not self.get_secure_cookie('user'):
            raise PermissionDenied()
        return fc(self, *args, **kwargs)

    return _


class LiveStreamHandler(ApplicationStartHandlerMixin, WebSocketHandler):
    # enable compression
    get_compression_options = lambda self: {}

    live_service = LiveService()

    subscribers = defaultdict(set)  # type: DefaultDict[int, Set[WebSocketHandler]]

    def open(self, *args, **kwargs):
        logger.debug('OPEN: {}'.format(self))
        self.set_nodelay(True)
        if self.get_secure_cookie('user'):
            self.write_message(dict(
                logged=True
            ))

    def on_close(self):
        logger.debug('CLOSE: {}'.format(self))
        self.unsubscribe(self)

    @transaction.atomic
    def on_message(self, message):
        try:
            data = json_decode(message)
        except ValueError as e:
            self.write_message(dict(
                success=False,
                message=str(e)
            ))
            return

        logger.debug("Message: %r", data)
        try:
            self._process_message(data)
        except ObjectDoesNotExist as e:
            self.write_message(dict(
                success=False,
                message=str(e)
            ))
        except PermissionDenied as e:
            self.write_message(dict(
                success=False,
                message='Not enough perms to perform action.'
            ))

    def _process_message(self, data: dict):
        logger.info('{}: {}'.format(data.get('action', '').upper(), data))
        if data.get('match'):
            self.subscribe_from_data(data=data)

        method = getattr(self, '_process_{}'.format(data.get('action')), None)
        if method:
            method(data)
        else:
            self.write_message(dict(
                success=False,
                message='Unknown action {}.'.format(data.get('action'))
            ))

    def subscribe_from_data(self, data):
        match = Match.objects.get(pk=data.get('match'))
        self.subscribe(match=match, subscriber=self)

    def _process_subscribe(self, data):
        match = Match.objects.get(pk=data.get('match'))
        self.write_message(dict(match=match.serialize()))

    @check_user
    def _process_goal(self, data):
        match, match_event = self.live_service.process_goal(data=data)
        self.notify(match, dict(
            event=match_event.serialize(),
            match=match.serialize(),
        ))

    @check_user
    def _process_state_change(self, data):
        match, event = self.live_service.process_state_change(data=data, notify_callback=self.notify)
        if not match:
            return

        data = dict(
            match=match.serialize(),
            event=event.serialize() if event else None
        )
        self.notify(match, {k: v for k, v in data.items() if v})

    def check_origin(self, origin):
        loc = urlparse(origin).netloc  # type: str
        return loc in settings.WS_ALLOWED_ORIGINS or loc.startswith('localhost') or loc.startswith('127.')

    @classmethod
    def on_application_start(cls, _: Application):
        """
        For all matches with required timer end plans callbacks to end half.
        """
        cls.live_service.plan_timers(notify_callback=cls.notify)

    @check_user
    def _process_delete_event(self, data):
        try:
            match = self.live_service.delete_event(data=data)
        except EventDeleteError as e:
            self.write_message(dict(
                match=e.match.serialize(),
                success=False,
            ))
            return

        self.notify(
            match,
            dict(
                match=match.serialize(),
                events=[
                    e.serialize() for e in match.match_match_event.all()
                ]
            )
        )

    @classmethod
    def notify(cls, match: Match, message: Union[dict, str]):
        logger.info('NOTIFY: {} subs, {}: {}'.format(
            len(cls.subscribers[match.id]),
            message.get('match', {}).get('id') or message.get('event', {}).get('id'),
            str(message)[:50]
        ))
        for sub in cls.subscribers[match.id]:  # type: WebSocketHandler
            sub.write_message(message)

    @classmethod
    def unsubscribe(cls, subscriber: WebSocketHandler, match: Match = None):
        if match and subscriber in cls.subscribers[match]:
            cls.subscribers[match.id].remove(subscriber)
            return
        for m in cls.subscribers.values():
            if subscriber in m:
                m.remove(subscriber)

    @classmethod
    def subscribe(cls, match: Match, subscriber: WebSocketHandler):
        cls.subscribers[match.id].add(subscriber)

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            dict(self.request.headers).get('User-Agent'),
        )
