<template>
    <div role="tablist">
        <b-card no-body class="mb-1" :title="team.name">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-btn block href="#" v-b-toggle="uniq(1)" variant="primary" class="text-uppercase">informace</b-btn>
            </b-card-header>
            <b-collapse :id="uniq(1, team.id)" visible :accordion="uniq(0)" role="tabpanel">
                <b-card-body>
                    <b-row>
                        <b-col class="font-weight-bold h5" cols="5">
                            {{ team.points }} b,
                            {{ team.order }}.
                            {{ team.scored }}:{{ team.received }}
                            ({{ (team.scored - team.received) > 0 ? '+' + (team.scored - team.received).toString() : (team.scored - team.received) }})
                        </b-col>
                        <b-col class="text-right">
                            {{ team.trainer_name }}<template v-if="team.trainer_name || team.dress_color">, </template>{{ team.dress_color }}
                        </b-col>
                    </b-row>

                    <hr class="clear">
                    <div v-html="
                        (team.description || '').trim().replace(/(\S+:)/g, '<strong>$1</strong>').replace(/(?:\r\n|\r|\n)/g, '<br>')
                    "></div>
                </b-card-body>
            </b-collapse>
        </b-card>

        <b-card no-body class="mb-1" v-if="team.players.length">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-btn block href="#" v-b-toggle="uniq(2)" variant="success" class="text-uppercase">soupiska</b-btn>
            </b-card-header>
            <b-collapse :id="uniq(2, team.id)" :accordion="uniq(0)" role="tabpanel">
                <b-list-group flush>
                    <b-list-group-item class="list-group-item-compact" v-for="player in team.players" :key="player.id">
                        <code>{{ player.number.pad(2) }}</code> {{ player.name }}
                        <span class="float-right">
                            <b-badge variant="primary">{{ player.match_goals }}</b-badge>
                            <b-badge>{{ player.total_goals }}</b-badge>
                        </span>
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
                    <b-list-group-item class="list-group-item-compact" v-for="match in team.matches" :key="match.id">
                        <template v-if="match.home_team_id === team.id">
                            <strong>{{ match.score[0] | score }}:{{ match.score[1] | score }}</strong> {{ match.away_team_name }}
                        </template>
                        <template v-else>
                            <strong>{{ match.score[1] | score }}:{{ match.score[0] | score }}</strong> {{ match.home_team_name }}
                        </template>
                        <span class="font-italic small float-right" v-if="!match.confirmed">
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
    .list-group-item-compact {
        padding: .40rem 1.25rem;
    }
</style>