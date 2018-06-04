<template>
    <div>
        <transition-group name="fade">
            <div v-if="loggedIn" key="isNotLoggedIn">
                <b-btn v-if="match.id" class="mt-2 ml-2 float-left" variant="warning" @click="resetMatch()">&times;</b-btn>
                <b-container fluid>
                    <transition name="fade">
                        <match-selector @change="openMatch($event.id)" v-if="!match.id"></match-selector>
                    </transition>
                    <hr v-if="!match.id">

                    <transition name="fade">
                        <match-overview v-if="match.id"></match-overview>
                    </transition>
                </b-container>
                <page-footer>
                    <a href="/">přenosy</a>
                </page-footer>
            </div>
            <div v-else key="isLoggedIn">
                <b-container>
                    <div style="height: 100vh;" class="row justify-content-center align-items-center">
                        <div class="col col-lg-5">
                            <login-form/>
                        </div>
                    </div>
                </b-container>
            </div>
        </transition-group>

        <div class="spinner">
            <spinner :enable="hasConnectionProblem" :invert="!loggedIn"/>
        </div>
    </div>
</template>

<script>
    import Spinner from './../base/components/Spinner'
    import MatchSelector from './components/MatchSelector'
    import LoginForm from './../base/components/LoginForm'
    import {mapActions, mapState, mapMutations} from 'vuex'
    import MatchOverview from "./components/MatchOverview";
    import PageFooter from "../base/components/Footer";

    export default {
        name: 'app',
        components: {
            PageFooter,
            MatchOverview,
            Spinner,
            LoginForm,
            MatchSelector
        },
        data() {
            return {matchId: 0}
        },
        methods: {
            ...mapActions(['openMatch', 'resetMatch']),
        },
        computed: {
            hasConnectionProblem() {
                return this.$store.state.socket.reconnectError || !this.$store.state.socket.isConnected;
            },
            ...mapState(['loggedIn', 'match'])
        },
        created() {
            if (window.location.hash)
                this.openMatch(window.location.hash.slice(1))
        }
    }
</script>

<style lang="scss">
    body {
        overflow-y: scroll;
        padding-bottom: 60px;
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

    .fade-enter-active, .fade-leave-active {
        transition-property: opacity;
        transition-duration: .2s;
    }

    .fade-enter-active {
        transition-delay: .2s;
    }

    .fade-enter, .fade-leave-active {
        opacity: 0
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
