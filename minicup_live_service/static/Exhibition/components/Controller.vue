<template>
    <div>
        <h1 class="text-center">{{ match.home_team_name }} vs. {{ match.away_team_name }}</h1>
        <h2 class="text-center">{{ match.score[0] | score }}:{{ match.score[1] | score }}</h2>
        <b-row>
            <b-col>
                <b-btn variant="primary" block @click="addHomeGoal">
                    +1
                </b-btn>
            </b-col>
            <b-col cols="2" class="text-center">
                <h2 class="text-center" v-if="isRunning">{{ timeFormatted }}</h2>
                {{ match.state | onlineStateName }}
            </b-col>
            <b-col>
                <b-btn variant="primary" block @click="addAwayGoal">
                    +1
                </b-btn>
            </b-col>
        </b-row>
        <hr>
        <b-row class="mt-2">
            <b-col>
                <b-form-input type="number" v-model="scoreHome"></b-form-input>
            </b-col>
            <b-col>
                <b-form-select v-model="state" :options="stateOptions" class="mb-3"></b-form-select>
            </b-col>
            <b-col>
                <b-form-input type="number" v-model="scoreAway"></b-form-input>
            </b-col>
        </b-row>
        <b-row class="mt-2" align-h="center">
            <b-col cols="4">
                <b-btn block variant="warning" @click="submit">SET</b-btn>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import {mapActions, mapMutations, mapState} from 'vuex';

    export default {
        name: "Controller",
        computed: {
            ...mapState(['match', 'serverTimeOffset']),
            timeFormatted() {
                return Math.floor(this.timerCount / 60).pad(2) + ':' + (this.timerCount % 60).pad(2);
            },
            isRunning() {
                return _.includes(['half_first', 'half_second'], this.match.state)
            }
        },
        data() {
            return {
                scoreHome: 0,
                scoreAway: 0,
                state: 'init',
                stateOptions: ['init', 'half_first', 'pause', 'half_second', 'end'],

                timerID: 0,
                timerCount: 0,
            }
        },
        methods: {
            ...mapActions(['addHomeGoal', 'addAwayGoal', 'submitMatch']),
            ...mapMutations(['setScore', 'setState']),
            submit() {
                this.setScore([
                    this.scoreHome,
                    this.scoreAway,
                ]);
                this.setState(this.state);
                this.submitMatch();
            }
        },
        created() {
            this.$store.watch(
                (state) => state.match.score,
                (new_, old) => {
                    [this.scoreHome, this.scoreAway] = new_;
                }
            );
            this.$store.watch(
                (state) => state.match.state,
                (new_, old) => {
                    this.state = new_;
                }
            );

            this.timerID = setInterval(() => {
                const start = this.match.second_half_start ? this.match.second_half_start : this.match.first_half_start;
                this.timerCount = Math.floor(Date.now() / 1000 - start + this.serverTimeOffset);
            }, 1000);
        },
        destroyed() {
            clearInterval(this.timerID);
        }
    }
</script>

<style scoped>

</style>