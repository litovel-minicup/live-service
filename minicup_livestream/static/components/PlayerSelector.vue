<template>
    <b-modal size="lg" id="modal" ref="modal" no-fade>
        <template slot="modal-title">Hráč z týmu <i>{{ name }}</i></template>

        <b-list-group class="players-list">
            <b-list-group-item
                    v-for="player in players"
                    :key="player.id"
                    class="d-flex align-items-center justify-content-between"
            >
                <span class="d-flex align-items-center">
                    <strong class="player-number display-4 text-right mr-2">
                        {{ player.number.pad(2) }}
                    </strong>
                    <strong class="mr-2">
                        {{ player.surname }}
                    </strong> {{ player.name }}
                </span>

                <b-button @click="goal(player)" variant="success">⚽</b-button>
            </b-list-group-item>
        </b-list-group>

        <template slot="modal-footer">
            <b-button @click="$refs.modal.hide()">zavřít</b-button>
        </template>
    </b-modal>
</template>

<script>
    export default {
        name: "player-selector",
        props: ['players', 'name'],
        methods: {
            show() {
                this.$refs.modal.show()
            },
            goal(player) {
                this.$emit('goal', {player: player.id});
                this.$refs.modal.hide();
            }
        }
    }
</script>

<style scoped>
    .players-list {
        overflow-y: scroll;
        max-height: 75vh;
    }

    .player-number {
        font-size: 2rem;
        font-weight: 300;
    }
</style>