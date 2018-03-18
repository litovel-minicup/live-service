<template>
    <div class="container">
        <match-header
                :match="match"
                :running.sync="running"
                @startTimer="running = true"
                @stopTimer="running = false"
        />

        <transition name="slide-top">
            <div class="row justify-content-between" v-if="running">
                <div class="col-5 text-right display-4">
                    <b-btn size="lg" variant="primary" block class="btn-score" @click="$refs.homeSelector.show()">
                        +1
                    </b-btn>
                </div>
                <div class="col-5 display-4">
                    <b-btn size="lg" variant="warning" block class="btn-score" @click="$refs.awaySelector.show()">
                        +1
                    </b-btn>
                </div>
            </div>
        </transition>


        <hr class="hr">

        <div class="row mt-4 justify-content-center">
            <div class="col-12">
                <match-events :events="events"/>
            </div>
        </div>

        <player-selector
                ref="homeSelector"
                @goal="goal"
                :name="match.home_team_name"
                :players="match.home_team_players"
        />
        <player-selector
                ref="awaySelector"
                @goal="goal"
                :name="match.away_team_name"
                :players="match.away_team_players"
        />
    </div>
</template>

<script>
    import MatchHeader from './MatchHeader'
    import MatchEvents from './MatchEvents'
    import PlayerSelector from './PlayerSelector'
    import {mapState} from 'vuex'

    export default {
        name: "match-detail",
        data() {
            return {
                running: false
            }
        },
        components: {
            MatchHeader,
            MatchEvents,
            PlayerSelector,
        },
        computed: {
            ...mapState([
                'match',
                'events'
            ]),
        },
        methods: {
            goal({player}) {
                console.log(player)
            }
        },
        beforeMount() {
            this.$store.dispatch('loadMatch', {match: this.$store.state.route.params.match});
            this.$store.dispatch('loadEvents', {match: this.$store.state.route.params.match})
        },

    }
</script>

<style scoped>

</style>