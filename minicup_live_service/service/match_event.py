# coding=utf-8
import string
from operator import itemgetter
from random import choice
from typing import Callable, Tuple

from vokativ import vokativ

from minicup_model.core.models import MatchEvent, Match, TeamInfo


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
    return sum(me.score) > 40


lots_of_goals_p = need_player(lots_of_goals)


def near_end(me, threshold=15):
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


def without_player_not_first(me: MatchEvent):
    is_first = me.score[me.match.teams.index(me.team_info)] == 1
    return not bool(me.player) and not is_first


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


def is_threshold_difference(threshold=10, positive=True):
    def _(me: MatchEvent):
        scorer_index = me.match.teams.index(me.team_info)
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
        (nth_match_goals_fulfill_p(1), '{player} otevírá gólový účet týmu {team}!'),
        (nth_match_goals_fulfill_p(1), '{player} poprvé rozvlnil{a} síť v tomto zápase!'),
        (nth_match_goals_fulfill_p(1), '{player} je úvodním střelcem svého týmu!'),

        (near_half_end_p, '{player} střílí gól do šatny!'),
        (near_half_end_p, '{player} se těsně před koncem poločasu prosazuje!'),
        (near_half_end_p, 'Gól před sirénou pro {player}!'),

        (nth_match_goals_fulfill_p(10), '{player} završuje první desítku gólů svého týmu!'),
        (nth_match_goals_fulfill_p(10), '{player} poprvé otevírá dvouciferné skóre svého týmu!'),
        (nth_match_goals_fulfill_p(20), '{player} střílí dvacátou branku pro tým {team}!'),
        (nth_match_goals_fulfill_p(20), '{player} završuje druhou desítku gólů svého týmu!'),
        (nth_match_goals_fulfill_p(30), '{player} se prosazuje třicátou brankou týmu {team}!'),
        (nth_match_goals_fulfill_p(30), '{player} završuje třetí desítku gólů pro tým {team}!'),

        (nth_player_goals_fulfill_p(1), 'I {player} se prosazuje!'),
        (nth_player_goals_fulfill_p(1), 'I {player} se přidává ke střelcům tohoto klání!'),
        (nth_player_goals_fulfill_p(5), '{player} předvádí své dovednosti pátou brankou!'),
        (nth_player_goals_fulfill_p(5), 'Pátý úspěšný pokus předvádí {player}!'),
        (nth_player_goals_fulfill_p(8), 'Střeleckou slinu nachází {player}!'),
        (nth_player_goals_fulfill_p(8), '{player} dnes pálí!'),
        (nth_player_goals_fulfill_p(10), 'Desátou brankou prokazuje {player} střeleckou formu!'),
        (nth_player_goals_fulfill_p(10), 'Střelec utkání {player} se prosazuje podesáté!'),
        (nth_player_goals_fulfill_p(10), '{player} ukazuje svoji exelentní střeleckou formu desátou brankou!'),
        (nth_player_goals_fulfill_p(15), 'Výbornou formu má dnes {player}!'),
        (nth_player_goals_fulfill_p(15), 'Čepice dolů, {player} střílí svou patnáctou branku v tomto utkání!'),
        (nth_player_goals_fulfill_p(15), 'Fantazie, {player} střílí svou patnáctou branku v tomto utkání!'),

        (match_score_p, 'Střela a {player} vyrovnává stav utkání!'),
        (match_score_p, '{player} srovnává stav tohoto utkání!'),
        (match_score, 'Máme tu shodu skóre!'),
        (match_score, 'Tým {team} srovnává stav zápasu!'),

        (is_lose_decrease_goal_p, '{player} snížil{a} stav utkání!'),
        (is_lose_decrease_goal_p, '{player} snižuje gólový deficit svého týmu!'),
        (is_win_increase_goal_p, '{player} navyšuje stav utkání!'),
        (is_win_increase_goal_p, '{player} navyšuje vedení týmu {team}!'),
        (is_win_increase_goal_p, '{player} vylepšuje stav utkání pro tým {team}!'),
        (lots_of_goals_p, 'K této kanonádě se přidává i {player}!'),
        (lots_of_goals_p, 'Další branku tohoto utkání bohatého na góly přidává i {player}!'),

        (anywhere_p, '{player} se prosazuje!'),
        (anywhere_p, 'Branku vsítil{a} {player}!'),
        (anywhere_p, 'Síť rozvlnil{a} {player}!'),
        (anywhere_p, '{player} upravuje stav utkání!'),
        (anywhere_p, '{player} to tam poslal{a}!'),
        (anywhere_p, '{player} se prosadil{a}!'),
        (anywhere_p, '{player} skóroval{a}!'),
        (anywhere_p, '{player} se přesvědčivě prosazuje!'),
        (anywhere_p, 'Výborně teď {player} prostřelil{a} brankáře!'),
        (anywhere_p, '{player} a úspěšná střela!'),
        (anywhere_p, 'Výborně, {first_v}!'),
        (anywhere_p, 'Pěkná branka, {first_v}!'),
        (anywhere_p, 'Pěkná střela, {first_v}!'),
        (anywhere_p, 'Pěkný gól, {first_v}!'),
        (anywhere_p, 'Pěkně vyřešeno, {first_v}!'),
        (anywhere_p, 'Excelentně, {first_v}!'),
        (anywhere_p, 'Dobře jsi to vymyslel{a}, {first_v}!'),
        (anywhere_p, 'Pěkně ses prosadil{a}, {first_v}!'),
        (anywhere_p, 'Výborně jsi to vyřešil{a}, {first_v}!'),
        (anywhere_p, 'Tak tohle se ti povedlo, {first_v}!'),
        (anywhere_p, 'Velmi dobře, {first_v}!'),
        (anywhere_p, 'Pěkně jsi to tam poslal{a}, {first_v}!'),
        (anywhere_p, 'Výborně vystřeleno, {first_v}!'),
        (anywhere_p, 'Pěkně jsi to trefil, {first_v}!'),

        (anywhere, 'Tým {team} se prosadil.'),
        (anywhere, 'Branka na účet týmu {team}.'),
        (anywhere, 'Brankář týmu {opposite_team} překonán.'),
        (anywhere, 'Tým {team} skóruje.'),
        (anywhere, 'Tým {team} se trefil.'),

        (is_win_threshold_difference_p, '{player} potvrzuje vedení týmu {team}!'),
        (is_win_threshold_difference_p, '{player} potvrzuje vysokou převahu týmu {team}!'),
        (is_win_threshold_difference_p, '{player} potvrzuje debakl týmu {opposite_team}!'),

        (is_lose_threshold_difference_p, '{player} snižuje z pohledu {team}!'),
        (is_lose_threshold_difference_p, '{player} snižuje golový deficit týmu {team}!'),
        (is_lose_threshold_difference_p, '{player} se snaží brankou zabránit debaklu týmu {team}!'),

        (without_player_not_first, 'Další branka na účet tohoto utkání.'),
        (without_player_not_first, 'Ukazatel skóre se opět mění.'),
        (without_player_not_first, 'Míč je opět v bráně.'),
        (without_player, 'Máme tu změnu skóre.'),
        (without_player, 'Tým {team} se prosazuje.'),
        (without_player, 'Změna stavu utkání.'),
        (without_player, 'Míč skončil v bráně.'),
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
                first_v=string.capwords(vokativ(player.name)) if player else '',
                team=match_event.team_info,
                opposite_team=tuple(set(match_event.match.teams) - {match_event.team_info})[0],
                a='a' if player and (player.surname.endswith('ová') or player.name.endswith('a')) else ''
            )
        return 'Změna stavu.'


__all__ = ['MatchEventMessageGenerator']
