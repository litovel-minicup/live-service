<template>
    <div class="match-events">
        <transition-group name="flip-list" tag="ul" class="list-group">
            <li
                    v-for="event in sorted"
                    :key="event.id"
                    class="list-group-item d-flex justify-content-between align-items-center"
            >
                <span>
                    <b-badge>{{ event.half_index + 1}}/2 | {{ event.time_offset | prettyTime }}</b-badge>
                    {{ event | eventMessage }} (<strong>{{ event.score[0] }}:{{ event.score[1] }}</strong>)
                </span>
                <button type="button" class="btn btn-danger" v-if="canDelete(event)" @click="deleteEvent(event)">
                    <span class="close">&times;</span>
                </button>
            </li>
        </transition-group>
    </div>
</template>

<script>
    export default {
        name: "events-list",
        props: ['match', 'events'],
        filters: {
            prettyTime(secs) {
                secs = Number(secs);
                return `${Math.floor(secs / 60).pad(2)}:${(secs % 60).pad(2)}`;
            },
            eventMessage(event) {
                if (event.message) return event.message;
                return `${{end: 'Konec', start: 'Začátek'}[event.type]} ${event.half_index + 1}. poločasu`;
            }
        },
        methods: {
            canDelete(event) {
                if (event.type !== 'goal') return false;
                // TODO: restrict to time
                const last = this.sorted[0];
                return last.id === event.id;
            },
            deleteEvent(event) {
                this.$store.dispatch('deleteEvent', event);
            }
        },
        computed: {
            sorted() {
                return _.reverse(_.sortBy(this.events, ['half_index'], ['time_offset']));
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