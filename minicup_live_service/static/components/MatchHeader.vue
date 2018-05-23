<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-6 text-right team-name" :title="match.home_team_name" :style="{ borderBottomColor: match.home_team_color }">
                {{ match.home_team_name }}
                <small class="dress-color font-weight-light text-muted" v-if="match.home_team_color_name">({{ match.home_team_color_name }})</small>
            </div>
            <div class="col-6 team-name" :title="match.away_team_name" :style="{ borderBottomColor: match.away_team_color }">
                {{ match.away_team_name }}
                <small class="dress-color font-weight-light text-muted" v-if="match.away_team_color_name">({{ match.away_team_color_name }})</small>
            </div>
        </div>
        <div class="row mt-2 justify-content-center">
            <transition name="scale-out" mode="out-in" tag="div" class="col-12 align-content-center text-center">
                <code class="display-4 text-center d-block" v-if="isRunning">
                    {{ timeFormatted }}
                </code>
                <div class="display-4 pb-1" v-if="!isRunning && matchState !== 'end'">
                    <b-btn variant="success" @click="start()">START</b-btn>
                </div>
            </transition>
        </div>
        <div class="row justify-content-center">
            <div class="col text-center display-5">
                {{ matchState | onlineStateName }}
            </div>
        </div>
        <div class="row no-gutters mt-2 d-flex align-items-center justify-content-center">
            <div class="col text-right display-4">
                <transition name="scale-out">
                    <b-btn v-if="isRunning" size="lg" variant="primary" block class="btn-score" @click="$emit('homeGoal')">
                        +1
                    </b-btn>
                </transition>
            </div>
            <div class="col display-4 text-center" style="font-family:monospace;">
                {{ match.score[0] | score }}:{{ match.score[1] | score }}
            </div>
            <div class="col display-4">
                <transition name="scale-out">
                    <b-btn v-if="isRunning" size="lg" variant="warning" block class="btn-score" @click="$emit('awayGoal')">
                        +1
                    </b-btn>
                </transition>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from 'vuex';

    export default {
        name: "match-header",
        props: ['match', 'running'],
        data() {
            return {
                timerCount: 0,
                timeoutID: -1
            }
        },
        methods: {
            start() {
                this.$store.dispatch('startHalf')
            }
        },
        filters: {
            score(val) {
                if (val === null) return '-';
                return val;
            }
        },
        computed: {
            ...mapState({
                matchState: (state) => state.match.state
            }),
            timeFormatted() {
                return Math.floor(this.timerCount / 60).pad(2) + ':' + (this.timerCount % 60).pad(2);
            },
            isRunning() {
                return this.matchState === 'half_first' || this.matchState === 'half_second'
            }
        },
        beforeMount() {
            this.$store.commit('connectFsmEvent', {
                event: '@start',
                cb: (evt, fsm) => {
                    this.timerCount = 0;
                    this.$emit('startTimer');
                },
            });

            this.$store.commit('connectFsmEvent', {
                event: '(pause end)',
                cb: (evt, fsm) => {
                    this.$emit('stopTimer');
                },
            });

            const timeoutCb = () => {
                const start = this.match.second_half_start ? this.match.second_half_start : this.match.first_half_start;
                this.timerCount = (Number(Date.now() / 1000) - start) | 0;

                if (
                    this.timerCount > this.$store.state.match.half_length &&
                    ['half_first', 'half_second'].indexOf(this.$store.state.fsm.state) >= 0
                ) {
                    this.$store.dispatch('endHalf').then(() => {
                        this.timerCount = 0
                    });
                }

            };
            this.timeoutID = setInterval(timeoutCb, 1000);
        },
        beforeDestroy() {
            clearInterval(this.timeoutID);
        }
    }
</script>

<style scoped lang="scss">
    .team-name {
        font-size: 2em;
        border-bottom: .15em solid #555 !important;
    }
    .dress-color {
        font-style: italic;
        font-size: .65em;
        display: block;
    }
</style>