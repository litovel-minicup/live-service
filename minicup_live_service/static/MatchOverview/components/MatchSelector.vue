<template>
    <div>
        <b-row class="mt-2">
            <b-col v-for="category in categories" :key="category.id">
                <b-btn block size="lg" @click="loadMatches({category: category.id})">{{ category.name }}</b-btn>
            </b-col>
        </b-row>
        <transition name="fade">
            <b-row class="mt-2" align-h="center" v-if="matches.length">
                <b-col>
                    <select v-model="match" class="form-control" @change="$emit('change', match)">
                        <option v-for="match_ in matches" :value="match_">
                            {{ match_.name }} | {{ match_.state | onlineStateName }} | {{ match_.date }}
                        </option>
                    </select>
                </b-col>
            </b-row>
        </transition>
    </div>
</template>

<script>

    import {mapActions, mapState} from 'vuex';

    export default {
        name: "MatchSelector",
        data() {
            return {
                match: {}
            }
        },
        methods: {
            ...mapActions(['loadCategories', 'loadMatches'])
        },
        computed: {
            ...mapState(['categories', 'matches'])
        },
        created() {
            this.loadCategories()
        }
    }
</script>

<style scoped>

</style>