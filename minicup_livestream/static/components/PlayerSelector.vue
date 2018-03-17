<template>
    <b-modal size="lg" id="modal" ref="modal" no-fade>
        <template slot="modal-title">Hráč z týmu <i>{{ name }}</i></template>

        <b-list-group>
            <b-list-group-item
                    v-for="player in players"
                    :key="player.id"
                    class="d-flex align-items-center justify-content-between"
            >
                <span class="d-flex align-items-center">
                    <strong class="player-number display-4 text-right mr-2">
                        {{ player.number | playerNumber(2) }}
                    </strong>
                    <strong class="mr-2">
                        {{ player.surname }}
                    </strong> {{ player.name }}
                </span>

                <b-button @click="goal(player.id)" variant="success">⚽</b-button>
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
        filters: {
            playerNumber(number, size) {
                let sign = Math.sign(number) === -1 ? '-' : '';
                return sign + new Array(size).concat([Math.abs(number)]).join('0').slice(-size);
            }
        },
        methods: {
            show() {
                this.$refs.modal.show()
            }
        }
    }
</script>

<style scoped>

</style>