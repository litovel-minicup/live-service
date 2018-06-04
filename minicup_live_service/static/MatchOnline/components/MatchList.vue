<template>
    <b-container>
        <h1>Výběr zápasu <b-btn v-if="location" class="mt-2 float-right" variant="warning" @click="location = ''">reset</b-btn></h1>
        <b-row v-if="!location" >
            <b-col v-for="k in locations" :key="k">
                <b-btn
                        block
                        variant="primary"
                        @click="location = k"
                    >
                    Hřiště {{ k }}
                </b-btn>
            </b-col>
        </b-row>
        <hr v-if="!location">
        <b-list-group>
            <b-list-group-item href="#"
                    @click="setMatch(m.id)"
                    v-for="m in nearestMatches"
                    :key="m.id"
            >
                <b-col>{{ m.name }}</b-col>
                <b-col class="text-right">{{ m.state | onlineStateName }} | {{ m.date }}</b-col>
            </b-list-group-item>
        </b-list-group>

        <v-loading v-if="!nearestMatches.length"></v-loading>

        <b-btn type="primary" block @click="count += 10" class="mt-4" v-if="count < filtered.length">Načíst další</b-btn>
    </b-container>
</template>

<script>
    import {mapState} from 'vuex'
    import _ from 'lodash'

    export default {
        name: "match-list",
        computed: mapState({
            matches: 'matches',
            filtered(state) {
                return _.filter(state.matches, (match) => {
                    return match.state !== 'end' && (!this.location || match.location === this.location);
                })
            },
            nearestMatches(state) {
                return _.slice(this.filtered, 0, this.count)
            },
            locations(state) {
                return _.uniq(_.map(this.nearestMatches, 'location'))
            },
            _: () => _
        }),
        data() {
            return {
                count: 10,
                location: '',
            }
        },
        methods: {
            setMatch(id) {
                this.$router.push({name: 'match', params: {match: id}});
            },
        },
        created() {
            this.$store.dispatch('loadMatches', {category: this.$route.params.category});
        }
    }
</script>

<style scoped>

</style>