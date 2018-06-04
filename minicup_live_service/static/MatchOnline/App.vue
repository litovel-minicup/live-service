<template>
    <div>
        <transition-group name="fade">
            <div v-if="loggedIn" key="isNotLoggedIn">
                <navigation key="navigation"/>
                <transition name="fade" mode="out-in">
                    <router-view key="router"/>
                </transition>
                <page-footer>
                    <a href="/overview">přehledy</a>
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
    import LoginForm from './../base/components/LoginForm'
    import Navigation from './components/Navigation'
    import {mapState} from 'vuex'
    import PageFooter from "../base/components/Footer";

    export default {
        name: 'app',
        components: {
            PageFooter,
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

    html {
        height: 100%;
        overflow: hidden;
    }

    body {
        height: 100%;
        overflow: auto;
        overflow-y: scroll !important;
    }
</style>
