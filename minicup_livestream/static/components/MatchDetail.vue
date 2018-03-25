<template>
    <div class="container">
        <match-header
                :match="match"
                :running.sync="running"
                @startTimer="running = true"
                @stopTimer="running = false"
                @homeGoal="$refs.homeSelector.show()"
                @awayGoal="$refs.awaySelector.show()"
        />

        <hr class="hr">

        <div class="row mt-4 justify-content-center">
            <div class="col-12">
                <match-events :events="events" :match="match"/>
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
        watch: {
            '$route'(to, from) {
                console.log(to, from, 'trololo')

            }
        },
        methods: {
            goal({player}) {
                this.$store.dispatch('goal', {player});
            }
        },
        beforeMount() {
            // TODO: refactor this.$store.state.route.params.match
            console.log('STATE: ', this.$store.state, this.match);
            this.$store.dispatch('openMatch', {match: this.$store.state.route.params.match});

            this.$store.commit('connectFsmEvent', {
                event: 'change',
                cb: (ev, fsm) => {
                    this.$store.dispatch('sendObj', {
                        action: 'state_change',
                        state: fsm.state,
                        match: this.$store.state.match.id
                    });
                }
            });
        },
    }
</script>

<style scoped>

</style>