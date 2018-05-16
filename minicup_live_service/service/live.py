# coding=utf-8
import logging
from datetime import datetime

from django.utils.timezone import now
from tornado.ioloop import IOLoop

from minicup_live_service.exceptions import EventDeleteError
from minicup_model.core.models import Match, TeamInfo, Player, MatchEvent
from .match_event import MatchEventMessageGenerator

logger = logging.getLogger(__name__)


class LiveService(object):
    match_event_message_generator = MatchEventMessageGenerator()

    def process_goal(self, data):
        match = Match.objects.get(pk=data.get('match'))
        team_info = TeamInfo.objects.get(pk=data.get('team'))

        try:
            player = Player.objects.get(pk=data.get('player'))
        except Player.DoesNotExist:
            player = None

        rivals = (match.home_team_info, match.away_team_info)
        if player and player.team_info != team_info:
            # TODO: problem
            logger.error('Player {} cannot score for team match {}.'.format(player, team_info))
            pass

        scores = [match.score_home or 0, match.score_away or 0]
        scores[rivals.index(team_info)] += 1
        # type: datetime
        starts = (match.first_half_start, match.second_half_start)
        half_start = max(filter(None, starts))

        # type: MatchEvent
        match_event = MatchEvent(
            match=match,
            player=player,
            team_info=team_info,
            type=MatchEvent.TYPE_GOAL,
            score_home=scores[0],
            score_away=scores[1],
            # not longer then half length
            time_offset=min((int((now() - half_start).total_seconds()), Match.HALF_LENGTH.total_seconds())),
            half_index=starts.index(half_start)
        )
        match_event.message = self.match_event_message_generator.generate(match_event=match_event)
        match_event.save()
        match.score_home, match.score_away = scores
        match.save()

        return match, match_event

    def process_state_change(self, data, notify_callback):
        match = Match.objects.get(pk=data.get('match'))
        state = data.get('state')

        event = match.change_state(state)
        if not event:
            return None, None

        if state == Match.STATE_HALF_FIRST:
            match.first_half_start = now()
            IOLoop.current().call_later(
                Match.HALF_LENGTH.total_seconds(),
                self._on_timer_end(match=match, notify_callback=notify_callback)
            )

        elif state == Match.STATE_HALF_SECOND:
            match.second_half_start = now()
            IOLoop.current().call_later(
                Match.HALF_LENGTH.total_seconds(),
                self._on_timer_end(match=match, notify_callback=notify_callback)
            )

        match.save(update_fields=('first_half_start', 'second_half_start',))
        return match, event

    def plan_timers(self, notify_callback):
        io_loop = IOLoop.current()
        for match in Match.objects.find_matches_with_required_timer():  # type: Match
            timer_end = ((match.second_half_start or match.first_half_start) + Match.HALF_LENGTH).timestamp()
            logging.info('MATCH {}: Planning timer end in {}.'.format(match.id, timer_end - io_loop.time()))
            io_loop.call_at(
                timer_end,
                self._on_timer_end(notify_callback=notify_callback, match=match)
            )

    @staticmethod
    def _on_timer_end(notify_callback, match: Match):
        def cb():
            event = match.on_timer_end()
            data = dict(match=match.serialize(), event=event.serialize() if event else None)
            notify_callback(match, {k: v for k, v in data.items() if v})

        return cb

    def delete_event(self, data):
        event = MatchEvent.objects.get(pk=data.get('event'))  # type: MatchEvent
        match = event.match
        logger.info('Deleting {}.'.format(event))
        before = match.match_match_event.exclude(pk=event.pk).last()  # type: MatchEvent

        if before:
            match.score_home, match.score_away = before.score
        else:
            match.score_home, match.score_away = 0, 0

        # TODO: old events cannot be deleted
        if match.confirmed:
            raise EventDeleteError(match=match)

        event.delete()
        match.save(update_fields=('score_home', 'score_away'))
        return match
