<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-6 text-right team-name" :title="match.home_team_name">
                {{ match.home_team_name }}
            </div>
            <div class="col-6 team-name" :title="match.away_team_name">
                {{ match.away_team_name }}
            </div>
        </div>
        <div class="row mt-2 justify-content-center">
            <transition name="scale-out" mode="out-in" tag="div" class="col-12 align-content-center text-center">
                <code class="display-4 text-center d-block mb-1" v-if="isRunning">
                    {{ timeFormatted }}
                </code>
                <div class="display-4" v-if="state === 's' || state === 'h'">
                    <b-btn variant="success" @click="start()">START</b-btn>
                </div>
            </transition>
        </div>
        <div class="row justify-content-center">
            <div class="col text-center display-5">
                <template v-if="state === 's'">
                    před zápasem
                </template>
                <template v-else-if="state === 'r1'">
                    1. poločas
                </template>
                <template v-else-if="state === 'h'">
                    v poločase
                </template>
                <template v-else-if="state === 'r2'">
                    2. poločas
                </template>
                <template v-else-if="state === 'e'">
                    po zápase
                </template>
            </div>
        </div>
        <div class="row no-gutters mt-2 d-flex align-items-center justify-content-center">
            <div class="col text-right display-4">
                <transition name="scale-out">
                    <b-btn v-if="running" size="lg" variant="primary" block class="btn-score" @click="$emit('homeGoal')">
                        +1
                    </b-btn>
                </transition>
            </div>
            <div class="col display-4 text-center" style="font-family:monospace;">
                {{ match.score[0] || '-' }}:{{ match.score[1] || '-' }}
            </div>
            <div class="col display-4">
                <transition name="scale-out">
                    <b-btn v-if="running" size="lg" variant="warning" block class="btn-score" @click="$emit('awayGoal')">
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
                return this.$store.state.fsm.state;
            },
            isRunning() {
                return this.state === 'r1' || this.state === 'r2'
            },
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
                event: '(h e)',
                cb: (evt, fsm) => {
                    this.enableTimer = false;
                    this.$emit('stopTimer');
                },
            });
            const timeoutCb = () => {
                if (this.enableTimer)
                    this.timerCount++;
                if (this.timerCount > 10) {
                    this.$store.dispatch('endHalf');
                    this.timerCount = 0;
                }

                this.timeoutID = setTimeout(timeoutCb, 1000);
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
    }
</style>