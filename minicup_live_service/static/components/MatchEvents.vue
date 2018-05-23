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
                    {{ event | eventMessage }}
                    <template v-if="event.type === 'goal'">
                        (<strong>{{ event.score[0] }}:{{ event.score[1] }}</strong>)
                    </template>
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
        name: "match-events",
        props: ['match', 'events'],
        filters: {
            prettyTime(secs) {
                secs = Number(secs);
                return `${Math.floor(secs / 60).pad(2)}:${(secs % 60).pad(2)}`;
            },
            eventMessage(event) {
                if (event.message) return event.message;
                return `${{end: 'Konec', start: 'Začátek'}[event.type]} ${event.half_index + 1}. poločasu.`;
            },
        },
        data() {
            return {
                time: new Date(),
                timerID: 0,
            }
        },
        methods: {
            canDelete(event) {
                if (event.type !== 'goal') return false;
                // TODO: threshold to live service API
                const last = this.sorted[0];
                return this.time < (new Date(event.absolute_time * 1000 + 60 * 1000)) && last.id === event.id;
            },
            deleteEvent(event) {
                if (!this.canDelete(event)) {
                    this.$toastr.w('Cannot be deleted.');
                    return;
                }
                this.$store.dispatch('deleteEvent', event);
            }
        },
        computed: {
            sorted() {
                return _.reverse(_.sortBy(this.events, ['half_index'], ['time_offset']));
            }
        },
        created() {
            this.timerID = setInterval(() => {
                this.time = new Date();
            }, 1000)
        },
        destroyed() {
            clearInterval(this.timerID);
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