<template>
    <div>
        <h1 class="text-center">
            {{ match.score[0] | score }}:{{ match.score[1] | score }}
            <br>
            <code v-if="isRunning">
                {{ timeFormatted }}
            </code>
        </h1>

        <h2 class="small text-center font-italic">{{ match.category_name }}, {{ match.state | onlineStateName }}</h2>
        <div class="clear"></div>

        <b-row>
            <b-col v-for="team in [homeTeamInfo, awayTeamInfo]" :key="team.id">
                <h2>{{ team.name }}</h2>
                <team-detail :team="team"></team-detail>
            </b-col>
        </b-row>
        <match-events :match="match" :events="events" :deletable="false"></match-events>
    </div>
</template>

<script>
    import {mapState} from 'vuex';
    import TeamDetail from "./TeamDetail";
    import MatchEvents from './../../base/components/MatchEvents'
    import _ from 'lodash';

    export default {
        name: "MatchOverview",
        components: {
            TeamDetail,
            MatchEvents,
        },
        data() {
            return {
                timeoutID: 0,
                timerCount: 0
            }
        },
        computed: {
            ...mapState(['match', 'events', 'homeTeamInfo', 'awayTeamInfo', 'serverTimeOffset']),
            timeFormatted() {
                return Math.floor(this.timerCount / 60).pad(2) + ':' + (this.timerCount % 60).pad(2);
            },
            halfIndex() {
                return !!this.match.first_half_start + !!this.match.second_half_start;
            },
            isRunning() {
                return _.includes(['half_first', 'half_second'], this.match.state)
            }
        },
        created() {
            this.timeoutID = setInterval(() => {
                const start = this.match.second_half_start ? this.match.second_half_start : this.match.first_half_start;
                this.timerCount = Math.floor(Date.now() / 1000 - start + this.serverTimeOffset);
            }, 1000);
        },
        beforeDestroy() {
            clearInterval(this.timeoutID);
        }
    }
</script>

<style scoped>

</style>