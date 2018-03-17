<template>
    <div class="container">
        <match-header :match="match"/>

        <hr class="hr">

        <div class="row justify-content-between">
            <div class="col-6 text-right display-4">
                <button class="btn btn-primary btn-block btn-lg btn-score" data-toggle="modal"
                        data-target="#modalHomePlayers">
                    +1
                </button>
            </div>
            <div class="col-6 display-4">
                <button class="btn btn-warning btn-block btn-lg btn-score" data-toggle="modal"
                        data-target="#modalAwayPlayers">
                    +1
                </button>
            </div>
        </div>

        <hr class="hr">
        <div class="row mt-4 justify-content-center">
            <div class="col-12">
                <match-events/>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal" id="modalHomePlayers" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">My team</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body players-list">
                        <ul class="list-group">
                            <li class="list-group-item d-flex align-items-center justify-content-between">
                                <span class="d-flex align-items-center">
                                    <strong class="player-number display-4 text-right mr-2">
                                        45
                                    </strong>
                                    <strong class="mr-2">
                                        My
                                    </strong> Name
                                </span>

                                <button v-on:click="goal(25)" type="button" class="btn btn-success">⚽
                                </button>
                            </li>
                        </ul>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">zavřít</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
    import MatchHeader from './MatchHeader'
    import MatchEvents from './MatchEvents'

    export default {
        name: "match-detail",
        components: {
            MatchHeader,
            MatchEvents,
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