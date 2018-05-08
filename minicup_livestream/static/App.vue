<template>
    <div>
        <div v-if="loggedIn">
            <navigation/>
            <router-view/>
        </div>
        <div v-else>
            <b-container>
                <div style="height: 100vh;" class="row justify-content-center align-items-center">
                    <div class="col col-lg-5">
                        <login-form/>
                    </div>
                </div>
            </b-container>
        </div>

        <div class="spinner">
            <spinner :enable="hasConnectionProblem"/>
        </div>
    </div>
</template>

<script>
    import Spinner from './components/Spinner'
    import LoginForm from './components/LoginForm'
    import Navigation from './components/Navigation'
    import {mapState} from 'vuex'

    export default {
        name: 'app',
        components: {
            Spinner,
            LoginForm,
            Navigation,
        },
        computed: {
            hasConnectionProblem() {
                return this.$store.state.socket.reconnectError || !this.$store.state.socket.isConnected;
            },
            ...mapState(['loggedIn'])
        },
        beforeMount() {
            // this.$toastr.defaultPosition = "toast-bottom-center";
            // this.$toastr.s("ERRROR MESSAGE");

            window.addEventListener('keydown', (e) => {
                this.$emit('keydown', e);
                console.log('emit');
            });
        },
        created() {

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

    .particles {

        position: absolute;
        top: 1em;
        bottom: 1em;
        left: 1em;
        right: 1em;
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
