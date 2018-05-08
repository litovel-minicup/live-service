# coding=utf-8
from operator import itemgetter
from random import choice
from typing import Callable, Tuple

from minicup_administration.core.models import MatchEvent, Match, TeamInfo


class Score(tuple):
    def __str__(self):
        return ':'.join(map(str, self))


Rule = Callable[[MatchEvent, ], bool]


def need_player(cb: Rule):
    def _(me: MatchEvent):
        if not me.player:
            return False
        return cb(me)

    return _


def lots_of_goals(me: MatchEvent):
    return sum(me.score) > 30


def near_end(me, threshold=20):
    return (Match.HALF_LENGTH.total_seconds() - me.time_offset) < threshold


near_half_end_p = need_player(near_end)


def nth_match_goals_fulfill_p(count):
    @need_player
    def _(me: MatchEvent):
        return me.score[me.match.teams.index(me.team_info)] == count

    return _


def nth_player_goals_fulfill_p(count):
    @need_player
    def _(me: MatchEvent):
        return me.match.match_match_event.filter(
            player=me.player,
            type=MatchEvent.TYPE_GOAL
        ).count() == count

    return _


def match_score(me: MatchEvent):
    return len(set(me.score)) == 1


match_score_p = need_player(match_score)


def anywhere(me: MatchEvent):
    return True


anywhere_p = need_player(anywhere)


def without_player(me: MatchEvent):
    return not bool(me.player)


def is_difference_change_match_event(positive):
    def _(me: MatchEvent):
        selected = sorted(
            enumerate(me.match.teams),
            key=lambda t: me.score[t[0]],
            reverse=positive
        )[0]  # type: Tuple[int, TeamInfo]
        return selected[1] == me.team_info

    return _


is_lose_decrease_goal = is_difference_change_match_event(positive=False)
is_lose_decrease_goal_p = need_player(is_lose_decrease_goal)

is_win_increase_goal = is_difference_change_match_event(positive=True)
is_win_increase_goal_p = need_player(is_win_increase_goal)


def is_threshold_difference(threshold=5, positive=True):
    def _(me: MatchEvent):
        teams = (me.match.home_team_info, me.match.away_team_info)
        scorer_index = teams.index(me.team_info)
        opposite_index = (1, 0)[scorer_index]
        if positive:
            return (me.score[scorer_index] - me.score[opposite_index]) > threshold
        else:
            return (me.score[opposite_index] - me.score[scorer_index]) > threshold

    return _


is_win_threshold_difference = is_threshold_difference()
is_lose_threshold_difference = is_threshold_difference(positive=False)

is_win_threshold_difference_p = need_player(is_win_threshold_difference)
is_lose_threshold_difference_p = need_player(is_lose_threshold_difference)


class MatchEventMessageGenerator(object):
    # ó
    MESSAGES = (
        (nth_match_goals_fulfill_p(1), '{player} otevírá gólový účet tohoto zápasu!'),
        (nth_match_goals_fulfill_p(1), '{player} poprvé rozvlnil sít v tomto zápase!'),

        (nth_player_goals_fulfill_p(1), 'I {player} se prosazuje!'),
        (nth_player_goals_fulfill_p(1), 'I {player} se přidává ke střelcům tohoto klání!'),

        (near_half_end_p, '{player} střílí gól do šatny!'),
        (near_half_end_p, '{player} se těsně před koncem poločasu prosazuje!'),
        (near_half_end_p, 'Gól před sirénou pro {player}!'),

        (nth_match_goals_fulfill_p(10), '{player} završuje první desítku gólů svého týmu!'),
        (nth_match_goals_fulfill_p(10), '{player} poprvé otevírá dvouciferné skore svého týmu!'),
        (nth_match_goals_fulfill_p(20), '{player} střílí dvacátou branku pro tým {team}!'),
        (nth_match_goals_fulfill_p(20), '{player} završuje druhou desítku gólů svého týmu!'),
        (nth_match_goals_fulfill_p(30), '{player} se prosazuje třicátou brankou týmu {team}!'),
        (nth_match_goals_fulfill_p(30), '{player} završuje třetí desítku gólů pro tým {team}!'),

        (nth_player_goals_fulfill_p(5), '{player} předvádí své dovednosti pátou brankou!'),
        (nth_player_goals_fulfill_p(5), 'Pátá branka v tomto utkání pro {player}!'),
        (nth_player_goals_fulfill_p(8), 'Střeleckou slinu našel {player}!'),
        (nth_player_goals_fulfill_p(10), 'Desátou brankou prokazuje {player} střeleckou formu!'),
        (nth_player_goals_fulfill_p(10), 'Střelec utkání {player} se prosazuje podesáté!'),

        (match_score_p, 'Střela a {player} vyrovnává stav utkání!'),
        (match_score_p, '{player} srovnává stav tohoto utkání!'),

        (is_lose_decrease_goal_p, '{player} snížil stav utkání!'),
        (is_lose_decrease_goal_p, '{player} snižuje gólový deficit svého týmu!'),
        (is_win_increase_goal_p, '{player} navyšuje stav utkání!'),
        (is_win_increase_goal_p, '{player} navyšuje vedení týmu {team}!'),
        (lots_of_goals, 'K této kanonádě se přidává i {player}!'),
        (lots_of_goals, 'Další branku tohoto utkání bohatého na góly přidává i {player}!'),

        (anywhere_p, '{player} se prosazuje!'),
        (anywhere_p, 'Branku vsítil {player}!'),
        (anywhere_p, 'Sít rozvlnil {player}!'),
        (anywhere_p, '{player} upravuje stav utkání!'),
        (anywhere_p, '{player} to tam poslal!'),
        (anywhere_p, '{player} se prosadil!'),
        (anywhere_p, '{player} skóroval!'),
        (anywhere_p, '{player} se přesvědčivě prosazuje!'),

        (is_win_threshold_difference_p, '{player} potvrzuje vedení týmu {team}!'),
        (is_win_threshold_difference_p, '{player} potvrzuje vysokou převahu týmu {team}!'),
        (is_win_threshold_difference_p, '{player} potvrzuje debakl týmu {opposite_team}!'),

        (is_lose_threshold_difference_p, '{player} snižuje z pohledu {team}!'),
        (is_lose_threshold_difference_p, '{player} snižuje golový deficit týmu {team}!'),
        (is_lose_threshold_difference_p, '{player} se snaží brankou zabránit debakl týmu {team}!'),

        (without_player, 'Další branka na účet tohoto utkání.'),
        (without_player, 'Máme tu změnu skóre.'),
        (without_player, 'Ukazatel skóre se opět mění.'),
        (without_player, 'Tým {team} se prosazuje.'),
        (without_player, 'Změna stavu utkání.'),
        (without_player, 'Míč je opět v bráně.'),
        (without_player, 'Tým {team} se prosazuje.'),
    )  # type: Tuple[Tuple[Rule, str]]

    def generate(self, match_event: MatchEvent):
        player = match_event.player

        filtered = tuple(
            map(
                itemgetter(1),
                filter(
                    itemgetter(0),
                    map(
                        lambda t: (t[0](match_event), t[1]),
                        self.MESSAGES
                    )
                )
            )
        )
        if filtered:
            return choice(filtered).format(
                player=player,
                team=match_event.team_info,
                opposite_team=tuple(set(match_event.match.teams) - {match_event.team_info})[0]
            )
        return 'Změna stavu.'


__all__ = ['MatchEventMessageGenerator']
