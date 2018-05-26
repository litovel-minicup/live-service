<template>
    <div class="container">
        <match-header
                :match="match"
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
                @goal="goal({player: $event, team:match.home_team_id})"
                :name="match.home_team_name"
                :players="match.home_team_players"
        />
        <player-selector
                ref="awaySelector"
                @goal="goal({player: $event, team:match.away_team_id})"
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
    import _ from 'lodash'

    export default {
        name: "match-detail",
        data() {
            return {

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
            goal({player, team}) {
                this.$store.dispatch('goal', {player, team});
            },
            loadMatch() {
                this.$store.dispatch('openMatch', {match: this.$route.params.match});
            }
        },
        created() {
            this.loadMatch();
            // plan refresh after connection lost
            this.$store.watch(
                (state) => {
                    return state.socket.isConnected;
                },
                (old, new_) => {
                    // plan match refresh && subscribe
                    !new_ && this.loadMatch();
                }
            );
            // connect state change of match
            // but only for first component.. not so clean solution, sorry
            // TODO: it's buggy, cannot be solved like this
            //_.once(() => {
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
            //});
        }
    }
</script>

<style scoped>

</style>