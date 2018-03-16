<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-6 text-right team-name" title="Home team">
                Home team
            </div>
            <div class="col-6 team-name" title="Away team">
                Away team
            </div>
        </div>
        <div class="row mt-2 justify-content-center">
            <code class="col-10 text-center display-4" v-if="playing">
                {{ timeFormatted }}
            </code>
            <div class="col-10 text-center display-5" v-else-if="!playing && halfIndex === 1">
                konec zápasu
            </div>
            <div class="col-10 text-center display-5" v-else-if="!playing && halfIndex == null">
                před zápasem
            </div>
            <div class="col-10 text-center" v-if="!playing && (halfIndex == null || halfIndex === 0)">
                <button class="btn btn-warning" v-on:click="start()">START</button>
            </div>
            <div class="col-10 text-center display-5" v-if="playing || (halfIndex === 0 && !playing)">
                {{ halfIndex + 1 }}. poločas
            </div>
        </div>
        <div class="row mt-2 justify-content-center">
            <div class="col-10 text-center display-4">
                {{ score[0] || '-' }} : {{ score[1] || '-' }}
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "match-header",
        props: [],
        data() {
            return {
                score: [null, null],
                playing: false,
                halfIndex: null,
            }
        },
        methods: {
            start() {
                this.playing = true;
            }
        },
        computed: {
            timeFormatted() {
                return '00:00'
            }
        }
    }
</script>

<style scoped>

</style>