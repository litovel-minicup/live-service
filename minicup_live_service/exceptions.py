# coding=utf-8


class EventDeleteError(RuntimeError):
    def __init__(self, match):
        self.match = match
