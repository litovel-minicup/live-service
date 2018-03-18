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



    .slide-top-enter-active {
        animation: bounce-in .5s;
    }

    .slide-top-leave-active {
        animation: bounce-in .5s reverse;
    }

    @keyframes bounce-in {
        0% {
            transform: translate(0, -500px);
        }
        100% {
            transform: translate(0, 0);
        }
    }
</style>
