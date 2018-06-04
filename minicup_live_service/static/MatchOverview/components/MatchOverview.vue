<template>
    <div>
        <h1 class="display-3 text-center">
            1/2
            <code>
                {{ timeFormatted }}
            </code>
            {{ match.score[0] | score }}:{{ match.score[1] | score }}
        </h1>
        <div class="clear"></div>
        <b-row>
            <b-col v-for="team in [homeTeamInfo, awayTeamInfo]" :key="team.id">
                <h2>{{ team.name }}</h2>
                <team-detail :team="team"></team-detail>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import {mapState} from 'vuex';
    import TeamDetail from "./TeamDetail";

    export default {
        name: "MatchOverview",
        components: {
            TeamDetail
        },
        computed: {
            ...mapState(['match', 'homeTeamInfo', 'awayTeamInfo']),
            timeFormatted() {
                return '00:00'
            }
        }
    }
</script>

<style scoped>

</style>