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
                <div class="display-4 pb-1" v-if="!isRunning && match.state !== 'end'">
                    <b-btn variant="success" @click="start()">START</b-btn>
                </div>
            </transition>
        </div>
        <div class="row justify-content-center">
            <div class="col text-center display-5">
                {{ match.state | onlineStateName }}
            </div>
        </div>
        <div class="row no-gutters mt-2 d-flex align-items-center justify-content-center">
            <div class="col text-right display-4">
                <transition name="scale-out">
                    <b-btn v-if="canScore" size="lg" variant="primary" block class="btn-score" @click="$emit('homeGoal')">
                        +1
                    </b-btn>
                </transition>
            </div>
            <div class="col display-4 text-center" style="font-family:monospace;">
                {{ match.score[0] | score }}:{{ match.score[1] | score }}
            </div>
            <div class="col display-4">
                <transition name="scale-out">
                    <b-btn v-if="canScore" size="lg" variant="warning" block class="btn-score" @click="$emit('awayGoal')">
                        +1
                    </b-btn>
                </transition>
            </div>
        </div>

        <b-modal
                size="xs"
                ref="modal"
                @ok="startHalf"
        >
            <template slot="modal-ok">Spustit čas</template>
            <template slot="modal-cancel">Ještě ne</template>
            <template slot="modal-title">Potvrzení časomíry</template>
            Opravdu chcete spustit časomíru? Spuštění časomíry je nevratné.
        </b-modal>
    </div>
</template>

<script>
    import {mapActions, mapState} from 'vuex';
    import _ from 'lodash';

    export default {
        name: "match-header",
        props: ['match'],
        data() {
            return {
                timerCount: 0,
                timeoutID: -1,
                canScore: false
            }
        },
        methods: {
            ...mapActions(['startHalf', 'endHalf']),
            start() {
                this.$refs.modal.show();
            }
        },
        computed: {
            ...mapState(['serverTimeOffset']),
            timeFormatted() {
                return Math.floor(this.timerCount / 60).pad(2) + ':' + (this.timerCount % 60).pad(2);
            },
            isRunning() {
                return _.includes(['half_first', 'half_second'], this.match.state)
            }
        },
        watch: {
            isRunning(new_, old) {
                !new_ && old && _.delay(() => {
                    if (!this.isRunning)
                        this.canScore = false;
                }, 1000 * 15);

                !old && new_ && (this.canScore = true);
            }
        },
        created() {
            /* this.$store.commit('connectFsmEvent', {
                event: '@start',
                cb: (evt, fsm) => {
                    // this.timerCount = 0;
                    console.warn(evt);
                    this.$emit('startTimer');
                },
            });

            this.$store.commit('connectFsmEvent', {
                event: '(pause end)',
                cb: (evt, fsm) => {
                    console.warn(evt);
                    this.$emit('stopTimer');
                },
            }); */
            this.canScore = this.isRunning;

            this.timeoutID = setInterval(() => {
                const start = this.match.second_half_start ? this.match.second_half_start : this.match.first_half_start;
                this.timerCount = Math.floor(Date.now() / 1000 - start + this.serverTimeOffset);

                if (
                    start != null &&
                    this.timerCount > this.match.half_length &&
                    _.includes(['half_first', 'half_second'], this.$store.state.fsm.state)
                ) {
                    this.endHalf().then(() => {
                        this.timerCount = 0
                    });
                }

            }, 1000);
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