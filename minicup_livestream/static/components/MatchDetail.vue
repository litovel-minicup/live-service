<template>
    <div class="container">
        <match-header :match="match"/>

        <hr class="hr">

        <div class="row justify-content-between">
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

        <hr class="hr">
        <div class="row mt-4 justify-content-center">
            <div class="col-12">
                <match-events/>
            </div>
        </div>

        <player-selector ref="homeSelector" :name="match.home_team_name" :players="match.home_team_players"/>
        <player-selector ref="awaySelector" :name="match.away_team_name" :players="match.away_team_players"/>
    </div>
</template>

<script>
    import MatchHeader from './MatchHeader'
    import MatchEvents from './MatchEvents'
    import PlayerSelector from './PlayerSelector'

    export default {
        name: "match-detail",
        components: {
            MatchHeader,
            MatchEvents,
            PlayerSelector,
        },
        computed: {
            match() {
                return this.$store.state.match;
            }
        },

        beforeMount() {
            this.$store.dispatch('loadMatch', {match: this.$store.state.route.params.match});
        }
    }
</script>

<style scoped>

</style>