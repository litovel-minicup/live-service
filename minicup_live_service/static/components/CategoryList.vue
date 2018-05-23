<template>
    <b-container>
        <h1>Výběr kategorie</h1>
        <div class="list-group">
            <a
                    class="list-group-item list-group-item-action"
                    @click="setCategory(cat.id)"
                    v-for="cat in categories"
            >
                {{ cat.name }}
            </a>
        </div>
    </b-container>
</template>

<script>
    import {mapActions, mapState} from 'vuex'

    export default {
        name: "category-list",
        computed: mapState(['categories']),
        methods: {
            setCategory(id) {
                this.$router.push({name: 'category', params: {category: id}});
            },
            ...mapActions(['loadCategories'])
        },
        created() {
            this.loadCategories()
        }
    }
</script>

<style scoped>

</style>