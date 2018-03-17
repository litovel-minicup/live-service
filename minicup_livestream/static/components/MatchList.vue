<template>
    <b-list-group class="list-group">
        <b-list-group-item href="#"
                @click="setMatch(m.id)"
                v-for="m in nearestMatches"
                :key="m.id"
        >
            {{ m.name }}
        </b-list-group-item>
    </b-list-group>
</template>

<script>
    import {mapState} from 'vuex'
    import _ from 'lodash'

    export default {
        name: "match-list",
        computed: mapState({
            matches: 'matches',
            nearestMatches(state) {
                return _.slice(this.$store.state.matches, 0, 10)
            }
        }),
        methods: {
            setMatch(id) {
                this.$router.push({name: 'match', params: {match: id}});
            }
        },
        beforeMount() {
            this.$store.dispatch('loadMatches', {category: this.$store.state.route.params.category});
        }
    }
</script>

<style scoped>

</style>