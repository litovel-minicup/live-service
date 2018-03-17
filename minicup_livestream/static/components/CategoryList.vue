<template>
    <ul class="list-group">
        <li
                class="list-group-item list-group-item-action"
                @click="setCategory(cat.id)"
                v-for="cat in categories"
        >
            {{ cat.name }}
        </li>
    </ul>
</template>

<script>
    import {mapState} from 'vuex'

    export default {
        name: "category-list",
        computed: mapState({
            categories: 'categories',
        }),
        methods: {
            setCategory(id) {
                this.$router.push({name: 'category', params: {category: id}});
            }
        },
        created() {
            this.$store.dispatch('loadCategories');
        }
    }
</script>

<style scoped>

</style>