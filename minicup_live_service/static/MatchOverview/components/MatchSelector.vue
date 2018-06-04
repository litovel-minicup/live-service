<template>
    <div>
        <b-row class="mt-2">
            <b-col
                    v-for="category_ in categories"
                    :key="category_.id"
            >
                <b-btn
                        block
                        size="lg"
                        @click="category = category_; loadMatches({category: category_.id})"
                        :variant="category_.id === category.id ? 'primary' : 'secondary' "
                >
                    {{ category_.name }}
                </b-btn>
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
        <v-loading v-if="category.id && !matches.length"></v-loading>
    </div>
</template>

<script>

    import {mapActions, mapState} from 'vuex';

    export default {
        name: "MatchSelector",
        data() {
            return {
                match: {},
                category: {}
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