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
            <transition name="slide-top">
                <code class="col-10 text-center display-4" v-if="isRunning">
                    {{ timeFormatted }}
                </code>
            </transition>
            <div class="col-10 text-center display-5">
                <b-btn variant="warning" @click="start()" v-if="state === 's' || state === 'h'">START</b-btn>
            </div>
            <div class="col-10 text-center display-5">
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
        <div class="row mt-2 justify-content-center">
            <div class="col-10 text-center display-4">
                {{ score[0] || '-' }} : {{ score[1] || '-' }}
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "match-header",
        props: ['match'],
        data() {
            return {
                score: [null, null],
                playing: false,
                halfIndex: null,
                timerCount: 0,
                enableTimer: false,
                timeoutID: -1
            }
        },
        methods: {
            start() {
                this.$store.commit('startTimer')
            }
        },
        computed: {
            timeFormatted() {
                return Math.round(this.timerCount / 60).pad(2) + ':' + (this.timerCount % 60).pad(2);
            },
            state() {
                return this.$store.state.fsm.state;
            },
            isRunning() {
                return this.state === 'r1' || this.state === 'r2'
            },
        },
        beforeMount() {
            this.$store.state.fsm.on('@start', (evt, fsm) => {
                this.enableTimer = true;
                this.$emit('startTimer');
            });
            this.$store.state.fsm.on('(h e)', (evt, fsm) => {
                this.enableTimer = false;
                this.$emit('stopTimer');
            });
            const timeoutCb = () => {
                if (this.enableTimer)
                    this.timerCount++;
                if (this.timerCount > 10) {
                    this.$store.commit('timerEnd');
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