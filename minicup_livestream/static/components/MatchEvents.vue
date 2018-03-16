<template>
    <div class="match-events">
        <ul class="list-group">
            <li v-for="event in events" class="list-group-item d-flex justify-content-between align-items-center">
                {{ event.timeOffset | prettyTime }}
                {{ event.message }}
                <button type="button" class="btn btn-danger"><span class="close">&times;</span></button>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "events-list",
        props: ['events']
    }
</script>

<style scoped>
    .match-events {
        overflow-y: scroll;
        /* height: 30 vh; */
    }
</style>