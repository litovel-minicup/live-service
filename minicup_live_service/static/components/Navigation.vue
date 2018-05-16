<template>
    <b-navbar toggleable="md">
        <b-container>
            <b-navbar-toggle target="navbar"/>
            <b-navbar-brand href='#' @click="$router.push({name: 'home'})">MC18 živé přenosy {{ $store.state.match.category_name }}</b-navbar-brand>
            <b-collapse is-nav id="navbar">
                <!-- <b-navbar-nav>
                    <b-nav-item href="#">Link</b-nav-item>
                    <b-nav-item href="#" disabled>Disabled</b-nav-item>
                </b-navbar-nav> -->

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto mr-4">
                    <b-nav-item @click="logout()">
                        Odhlásit se
                    </b-nav-item>
                    <b-nav-item @click="$router.back()">
                        Zpět
                    </b-nav-item>
                    <!--
                    <b-nav-form>
                        <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Search"/>
                        <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
                    </b-nav-form>

                    <b-nav-item-dropdown text="Lang" right>
                        <b-dropdown-item href="#">EN</b-dropdown-item>
                        <b-dropdown-item href="#">ES</b-dropdown-item>
                        <b-dropdown-item href="#">RU</b-dropdown-item>
                        <b-dropdown-item href="#">FA</b-dropdown-item>
                    </b-nav-item-dropdown>

                    <b-nav-item-dropdown right>
                        <template slot="button-content">
                            <em>User</em>
                        </template>
                        <b-dropdown-item href="#">Profile</b-dropdown-item>
                        <b-dropdown-item href="#">Signout</b-dropdown-item>
                    </b-nav-item-dropdown>
                    -->
                </b-navbar-nav>

            </b-collapse>
        </b-container>
    </b-navbar>
</template>

<script>
    export default {
        methods: {
            logout() {
                this.$store.dispatch('logout').then(() => {
                    this.$toastr.i('Logout successful.');
                });
            }
        }
    }
</script>

<style scoped lang="scss">
    .navbar {
        background-color: #4180ff;
        .nav-link, .navbar-brand {
            color: white;
        }
    }
</style>