<template>
    <div>
        <transition-group name="fade">
            <div v-if="loggedIn" key="isNotLoggedIn">
                <b-container>
                    <controller></controller>
                </b-container>
                <page-footer></page-footer>
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
    import {mapState} from 'vuex'
    import PageFooter from "../base/components/Footer";
    import Controller from "./components/Controller";

    export default {
        name: 'app',
        components: {
            Controller,
            PageFooter,
            Spinner,
            LoginForm
        },
        computed: {
            hasConnectionProblem() {
                return this.$store.state.socket.reconnectError || !this.$store.state.socket.isConnected;
            },
            ...mapState(['loggedIn', 'match'])
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
</style>
