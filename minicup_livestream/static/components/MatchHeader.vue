<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-6 text-right team-name" :title="match.home_team_name" :style="{ borderBottomColor: match.home_team_color }">
                <small class="font-weight-light text-muted font-italic" v-if="match.home_team_color_name">({{ match.home_team_color_name }})</small>
                {{ match.home_team_name }}
            </div>
            <div class="col-6 team-name" :title="match.away_team_name" :style="{ borderBottomColor: match.away_team_color }">
                {{ match.away_team_name }}
                <small class="font-weight-light text-muted font-italic" v-if="match.away_team_color_name">({{ match.away_team_color_name }})</small>
            </div>
        </div>
        <div class="row mt-2 justify-content-center">
            <transition name="scale-out" mode="out-in" tag="div" class="col-12 align-content-center text-center">
                <code class="display-4 text-center d-block" v-if="isRunning">
                    {{ timeFormatted }}
                </code>
                <div class="display-4 pb-1" v-if="!isRunning && state !== 'end'">
                    <b-btn variant="success" @click="start()">START</b-btn>
                </div>
            </transition>
        </div>
        <div class="row justify-content-center">
            <div class="col text-center display-5">
                {{ state | onlineStateName }}
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
                {{ match.score[0] || '-' }}:{{ match.score[1] || '-' }}
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
    export default {
        name: "match-header",
        props: ['match', 'running'],
        data() {
            return {
                timerCount: 0,
                enableTimer: false,
                timeoutID: -1
            }
        },
        methods: {
            start() {
                this.$store.dispatch('startHalf')
            }
        },
        computed: {
            timeFormatted() {
                return Math.floor(this.timerCount / 60).pad(2) + ':' + (this.timerCount % 60).pad(2);
            },
            state() {
                return this.$store.state.match.state;
            },
            isRunning() {
                return this.state === 'half_first' || this.state === 'half_second'
            }
        },
        beforeMount() {
            this.$store.commit('connectFsmEvent', {
                event: '@start',
                cb: (evt, fsm) => {
                    this.enableTimer = true;
                    this.$emit('startTimer');
                },
            });

            this.$store.commit('connectFsmEvent', {
                event: '(pause end)',
                cb: (evt, fsm) => {
                    this.enableTimer = false;
                    this.$emit('stopTimer');
                },
            });

            console.log("Match: ", this.match);
            const timeoutCb = () => {
                clearInterval(this.timeoutID);
                this.timeoutID = setTimeout(timeoutCb, 1000);
                // if (!this.enableTimer) return;

                const start = this.match.second_half_start ? this.match.second_half_start : this.match.first_half_start;
                this.timerCount = (Number(Date.now() / 1000) - start) | 0;

                if (this.timerCount > this.$store.state.match.half_length) {
                    this.$store.dispatch('endHalf').then(() => {
                        this.timerCount = 0
                    });
                }

            };
            this.timeoutID = setTimeout(timeoutCb, 1000);
        },
        beforeDestroy() {
            clearInterval(this.timeoutID);
        }
    }
</script>

<style scoped lang="scss">
    .team-name {
        font-size: 2em;
        border-bottom: .2em solid;
    }
</style>