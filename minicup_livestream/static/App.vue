<template>
    <div class="container">
        <router-view/>
    </div>
</template>

<script>
    export default {
        name: 'app',
        beforeMount() {
            this.$socket.onopen = () => {
                this.$socket.sendObj({
                    action: 'matches'
                })
            }
        }
    }
</script>

<style>
    body {
        overflow-y: scroll;
    }

    .btn-score {
        padding: 25px;
        font-size: 2.25rem;
    }

    html {
        height: 100%;
        overflow: hidden;
    }

    body {
        height: 100%;
        overflow: auto;
    }

    .players-list {
        overflow-y: scroll;
        max-height: 75vh;
    }

    .player-number {
        font-size: 2rem;
        font-weight: 300;
    }
</style>
