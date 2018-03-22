# coding=utf-8
from random import choice

from minicup_administration.core.models import MatchEvent


class Score(tuple):
    def __str__(self):
        return ':'.join(map(str, self))


class MatchEventMessageGenerator(object):
    import vokativ.vokativ
    # ó
    MESSAGES = (
        # TODO: conditions
        (lambda me: True, '{player} snížil stav utkání!'),
        (lambda me: True, '{player} navyšuje stav utkání!'),
        (lambda me: True, 'Střela a {player} vyrovnává stav utkání!'),
        (lambda me: True, '{player} se prosadil!'),
        (lambda me: True, 'Branku vsítil {player}!'),
        (lambda me: True, 'Sít rozvlnil {player}!'),
        (lambda me: True, '{player} upravuje stav utkání!'),
        (lambda me: True, '{player} to tam poslal!'),
        (lambda me: True, '{player} se prosadil!'),
        (lambda me: True, '{player} skóroval!'),
        (lambda me: True, '{player} potvrzuje dominanci domácích/hostů!'),
        (lambda me: True, '{player} potvrzuje debakl domácích/hostů!'),
        (lambda me: True, '{player} se přesvědčivě prosazuje!'),
        (lambda me: True, '{player} otevírá gólový účet tohoto zápasu!'),
        (lambda me: True, '{player} střílí gól do šatny!'),
        (lambda me: True, 'I {player} se prosazuje!'),
        (lambda me: True, 'K této kanonádě se přidává i {player}!'),
        (lambda me: True, 'I {player} se přidává ke střelcům tohoto klání!'),
        (lambda me: True, 'Gól před sirénou pro {player}.'),
        (lambda me: True, '{player} završuje první desítku gólů svého týmu.'),
        (lambda me: True, '{player} završuje druhou desítku gólů svého týmu.'),
    )

    def generate(self, match_event: MatchEvent):
        player = match_event.player
        scores = match_event.score_home, match_event.score_away

        return choice(self.MESSAGES)[1].format(player=player)
