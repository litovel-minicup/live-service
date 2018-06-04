<template>
    <div role="tablist">
        <b-card no-body class="mb-1" :title="team.name">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-btn block href="#" v-b-toggle="uniq(1)" variant="primary" class="text-uppercase">informace</b-btn>
            </b-card-header>
            <b-collapse :id="uniq(1, team.id)" visible :accordion="uniq(0)" role="tabpanel">
                <b-card-body>
                    <b-row class="font-weight-bold h4">
                        <b-col>{{ team.points }} b</b-col>
                        <b-col>{{ team.order }}</b-col>
                        <b-col cols="6">{{ team.scored }}:{{ team.received }} ({{ team.scored - team.received }})</b-col>
                    </b-row>
                    {{ team.trainer_name }} <span class="float-right">{{ team.dress_color }}</span>
                </b-card-body>
            </b-collapse>
        </b-card>
        <b-card no-body class="mb-1" v-if="team.players.length">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-btn block href="#" v-b-toggle="uniq(2)" variant="success" class="text-uppercase">soupiska</b-btn>
            </b-card-header>
            <b-collapse :id="uniq(2, team.id)" :accordion="uniq(0)" role="tabpanel">
                <b-list-group flush>
                    <b-list-group-item v-for="player in team.players">
                        <code>{{ player.number.pad(2) }}</code> {{ player.name }}
                        <b-badge class="float-right">{{ player.goals_count }}</b-badge>
                    </b-list-group-item>
                </b-list-group>
            </b-collapse>
        </b-card>
        <b-card no-body class="mb-1">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-btn block href="#" v-b-toggle="uniq(3)" variant="warning" class="text-uppercase">zápasy</b-btn>
            </b-card-header>
            <b-collapse :id="uniq(3)" :accordion="uniq(0)" role="tabpanel">
                <b-list-group flush>

                    <b-list-group-item v-for="match in team.matches">
                        <template v-if="match.home_team_id === team.id">
                            {{ match.score[0] | score }}:{{ match.score[1] | score }} {{ match.away_team_name }}
                        </template>
                        <template v-else>
                            {{ match.score[1] | score }}:{{ match.score[0] | score }} {{ match.home_team_name }}
                        </template>
                        <span class="font-italic small" v-if="!match.confirmed">
                            (nepotvrzeno)
                        </span>
                    </b-list-group-item>

                </b-list-group>
            </b-collapse>
        </b-card>
    </div>
</template>

<script>
    export default {
        name: "TeamDetail",
        props: ['team'],
        methods: {
            uniq(n) {
                return `${this._uid}-${n}`;
            }
        }
    }
</script>

<style scoped>

</style>