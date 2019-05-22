# coding=utf-8
from datetime import datetime, timedelta
from json import loads

from minicup_model.core.models import TeamInfo, Match, Category, MatchTerm, Day
from .base import BaseWebsocketHandler
from ..service.live import LiveService


class ExhibitionLiveStreamHandler(BaseWebsocketHandler):
    subs = set()

    day = Day.objects.filter(
        year__slug='2019',
        day=datetime(2019, 5, 31).date()
    ).first()

    category = Category(
        id=1,
        name='Exhibice',
        slug='exhibice',
        year=day.year
    )

    match_term = MatchTerm(
        id=1,
        day=day,
        start=datetime(2019, 5, 31, 19, 00)
    )

    home = TeamInfo(
        id=1,
        category=category,
        name='Tatran Litovel',
        abbr='LIT',
        slug='tatran-litovel',
        color_primary='#0d5499',
        color_secondary='#FFFFFF',
        color_text='#0d5499',
    )

    away = TeamInfo(
        id=2,
        category=category,
        name='Výběr trenérů a rozhodčích',
        abbr='MC',
        slug='litovel-minicup',
        color_primary='#00359e',
        color_secondary='#FFFFFF',
        color_text='#00359e',
    )

    match = Match(
        id=1,
        category=category,
        home_team_info=home,
        away_team_info=away,
        online_state=Match.STATE_INIT,
        score_home=0,
        score_away=0,
        match_term=match_term,
    )
    match.half_length = timedelta(minutes=30)

    def dump_match(self):
        data = dict(
            type_content=[LiveService.MESSAGE_CONTENT_MATCH],
            match=self.match.serialize(),
        )
        for sub in self.subs:
            sub.write_message(data)

    def dump_players(self):
        for team in (self.home, self.away):
            data = dict(
                type_content=[LiveService.MESSAGE_CONTENT_TEAM_PLAYERS],
                players=[],
                team=team.id,
            )
            for sub in self.subs:
                sub.write_message(data)

    def open(self, *args, **kwargs):
        self.subs.add(self)
        if self.get_secure_cookie('user'):
            self.write_message(dict(
                logged=True
            ))
        self.dump_match()
        self.dump_players()

    def on_close(self):
        self.subs.discard(self)

    def on_message(self, message):
        data = loads(message)

        match = data.get('match_obj')

        if match:
            self.match.score_home = match.get('score')[0]
            self.match.score_away = match.get('score')[1]
            new_state = match.get('state')
            if new_state != self.match.online_state:
                if new_state == Match.STATE_HALF_FIRST:
                    self.match.first_half_start = datetime.now()
                elif new_state == Match.STATE_HALF_SECOND:
                    self.match.second_half_start = datetime.now()
                elif new_state == Match.STATE_INIT:
                    self.match.second_half_start = self.match.first_half_start = None
            self.match.online_state = match.get('state')

        self.dump_match()

    def write_message(self, message, *args, **kwargs):
        if isinstance(message, dict):
            message['server_time'] = datetime.now().timestamp()
            message.setdefault('type_content', []).append(LiveService.MESSAGE_CONTENT_SERVER_TIME)

        return super().write_message(message, *args, **kwargs)
