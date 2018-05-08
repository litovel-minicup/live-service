# coding=utf-8
from django.shortcuts import get_object_or_404

from minicup_administration.core.models import Category, Match, TeamInfo
from minicup_livestream.handlers.base import AuthenticatedBaseHandler


class CategoryListHandler(AuthenticatedBaseHandler):
    def get(self):
        self.write(dict(categories=[
            dict(
                id=c.id,
                name='{} - {}'.format(c.year, c)
            ) for c in Category.objects.filter(match_category__confirmed__isnull=True).distinct()
        ]))


class MatchListHandler(AuthenticatedBaseHandler):
    def get(self, category_id):
        self.write(dict(matches=[
            dict(
                id=m.id,
                name=str(m),
                date=str(m.match_term),
                state=m.online_state
            ) for m in Match.objects.filter(
                category_id=category_id,
                confirmed__isnull=True,
            )
        ]))


class MatchHandler(AuthenticatedBaseHandler):
    def get(self, match_id):
        match = get_object_or_404(Match, pk=match_id)  # type: Match

        def players(team_info: TeamInfo):
            return [
                dict(
                    id=p.id,
                    name=p.name,
                    surname=p.surname,
                    number=p.number
                ) for p in team_info.team_info_player.all()
            ]

        self.write(match.serialize(
            home_team_players=players(match.home_team_info),
            away_team_players=players(match.away_team_info),
        ))


class MatchEventsHandler(AuthenticatedBaseHandler):
    def get(self, match_id):
        match = get_object_or_404(Match, pk=match_id)

        self.write(dict(
            events=[
                me.serialize() for me in match.match_match_event.all()
            ]
        ))
