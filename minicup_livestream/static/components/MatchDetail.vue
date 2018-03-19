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
                this.$socket.sendObj({
                    action: 'goal',
                    match: this.match.id,
                    player: player,
                });
            }
        },
        beforeMount() {
            this.$store.dispatch('loadMatch', {match: this.$store.state.route.params.match});
            this.$store.dispatch('loadEvents', {match: this.$store.state.route.params.match});

            this.$options.sockets.onopen = (context) => {
                this.$socket.sendObj({
                    match: this.$store.state.route.params.match,
                    action: 'subscribe'
                });
            };
        },
    }
</script>

<style scoped>

</style>