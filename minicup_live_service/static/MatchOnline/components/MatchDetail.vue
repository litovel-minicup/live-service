<template>
    <b-container>
        <match-header
                :match="match"
                @homeGoal="$refs.homeSelector.show()"
                @awayGoal="$refs.awaySelector.show()"
        />

        <hr>

        <div class="row mt-4 justify-content-center">
            <div class="col-12">
                <match-events :events="events" :match="match"/>
            </div>
        </div>

        <player-selector
                ref="homeSelector"
                @goal="goal({player: $event, team: match.home_team_id})"
                v-on:goal="match.score[0]++"
                :name="match.home_team_name"
                :players="match.home_team_players"
        />
        <player-selector
                ref="awaySelector"
                @goal="goal({player: $event, team: match.away_team_id})"
                v-on:goal="match.score[1]++"
                :name="match.away_team_name"
                :players="match.away_team_players"
        />
    </b-container>
</template>

<script>
    import MatchHeader from './MatchHeader'
    import MatchEvents from './../../base/components/MatchEvents'
    import PlayerSelector from './PlayerSelector'
    import {mapActions, mapState} from 'vuex'

    export default {
        name: "match-detail",
        data() {
            return {}
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
            ...mapActions(['unsubscribeMatch', 'goal', 'openMatch']),
            registerFsmListener() {
                if (this.$store.state.fsmStateChangeListenerRegistered) return;

                this.$store.commit('setFsmStateChangeListenerRegistered');
                this.$store.commit('connectFsmEvent', {
                    event: 'change',
                    cb: (ev, fsm) => {
                        if (this.match.state === fsm.state)
                            return;

                        this.$store.dispatch('sendObj', {
                            action: 'state_change',
                            state: fsm.state,
                            match: this.$store.state.match.id
                        });
                    }
                });
            }
        },
        created() {
            this.openMatch(Number(this.$route.params.match));
            // plan refresh after connection lost
            this.$store.watch(
                (state) => {
                    return state.socket.isConnected;
                },
                (new_, old) => {
                    // plan match refresh && subscribe
                    !old && new_ && this.openMatch();
                }
            );
            // connect state change of match
            // but only for first component.. not so clean solution, sorry
            this.registerFsmListener();
        },
        beforeDestroy() {
            this.unsubscribeMatch({match: this.match.id});
        }
    }
</script>

<style scoped>

</style>