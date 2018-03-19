<template>
    <div>
        <div class="spinner">
            <spinner :enable="enabled"/>
        </div>
        <b-container>
            <router-view/>
        </b-container>
    </div>
</template>

<script>
    import Spinner from './components/Spinner'

    export default {
        name: 'app',
        components: {
            Spinner
        },
        computed: {
            enabled() {
                return this.$store.state.socket.reconnectError || !this.$store.state.socket.isConnected;
            }
        }
    }
</script>

<style lang="scss">
    body {
        overflow-y: scroll;
    }

    .spinner {
        position: fixed;
        left: calc(100% - 80px);
        top: 0;
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
        overflow-y: scroll !important;
    }

    .slide-top-enter-active {
        animation: bounce-in .5s;
    }

    .slide-top-leave-active {
        animation: bounce-in .5s reverse;
    }

    .scale-out-enter-active {
        animation: scale-out 300ms;
    }

    .scale-out-leave-active {
        animation: scale-out 300ms reverse;
    }

    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }

    @keyframes bounce-in {
        0% {
            transform: translate(0, -500px);
        }
        100% {
            transform: translate(0, 0);
        }
    }

    @keyframes scale-out {
        0% {
            transform: scale(0, 0);
        }
        80% {
            transform: scale(1.2, 1.2);
        }
        100% {
            transform: scale(1, 1);
        }
    }
</style>
