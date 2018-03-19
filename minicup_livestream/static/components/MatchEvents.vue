<template>
    <div class="match-events">
        <transition-group name="flip-list" tag="ul" class="list-group">

            <li
                    v-for="event in sorted"
                    :key="event.id"
                    class="list-group-item d-flex justify-content-between align-items-center">
                <span>
                    <b-badge>{{ event.timeOffset | prettyTime }}</b-badge>
                {{ event.message }}
                    </span>
                <button type="button" class="btn btn-danger"><span class="close">&times;</span></button>
            </li>
        </transition-group>
    </div>
</template>

<script>
    export default {
        name: "events-list",
        props: ['events'],

        filters: {
            prettyTime(secs) {
                secs = Number(secs);
                return Math.floor(secs / 60).pad(2) + ':' + (secs % 60).pad(2);
            },
        },
        computed: {
            sorted() {
                return _.reverse(_.sortBy(this.events, ['halfIndex'], ['timeOffset']));
            }
        }
    }
</script>

<style scoped>
    .match-events {
        overflow-y: scroll;
        /* height: 30 vh; */
    }

    .flip-list-move {
        transition: transform 1s;
    }
</style>