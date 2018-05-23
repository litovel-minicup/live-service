<template>
    <b-container>
        <h1>Výběr zápasu</h1>
        <b-list-group class="list-group">
            <b-list-group-item href="#" class="row"
                    @click="setMatch(m.id)"
                    v-for="m in nearestMatches"
                    :key="m.id"
            >
                <b-col>{{ m.name }}</b-col>
                <b-col class="text-right">{{ m.state | onlineStateName }} | {{ m.date }}</b-col>
            </b-list-group-item>
        </b-list-group>

        <b-btn type="primary" block @click="count += 10" class="mt-4">Načíst další</b-btn>
    </b-container>
</template>

<script>
    import {mapState} from 'vuex'
    import _ from 'lodash'

    export default {
        name: "match-list",
        computed: mapState({
            matches: 'matches',
            nearestMatches(state) {
                return _.slice(this.filtered, 0, this.count)
            },
            filtered(state) {
                return _.filter(state.matches, (match) => {
                    return match.state !== 'end';
                })
            }
        }),
        data() {
            return {
                count: 10
            }
        },
        methods: {
            setMatch(id) {
                this.$router.push({name: 'match', params: {match: id}});
            }
        },
        created() {
            this.$store.dispatch('loadMatches', {category: this.$store.state.route.params.category});
        }
    }
</script>

<style scoped>

</style>