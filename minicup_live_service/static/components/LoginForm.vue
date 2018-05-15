<template>
    <div class="login-form" @click="click">
        <div class="row mb-2 justify-content-center">
            <div class="col-4">
                <form class="form" @submit.prevent="send">
                    <label>
                        <input type="password" ref="pin" v-model="pin" autofocus class="form-control">
                        <br>
                        <input type="submit" class="form-control" value="Login">
                    </label>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "login-form",
        methods: {
            click(ev) {
                if ((/\d/).test(ev.toElement.textContent))
                    this.pin += ev.toElement.textContent;
            },
            send() {
                this.$store.dispatch('login', {
                    pin: this.pin,
                }).then(() => {
                    if (!this.$store.state.loggedIn) {
                        this.$toastr.w('Incorrect PIN.');
                        this.pin = '';
                    } else {
                        this.$toastr.i('Logged in.');
                    }
                });
            }
        },
        data() {
            return {
                pin: ''
            }
        },
        beforeMount() {
            this.$root.$on('keydown', (e) => {
                this.pin += e.key;
            });
        }
    }
</script>

<style scoped lang="scss">
    $light: transparentize(#bbbbbb, 0.1);

    .login-form {
        border: 1px solid $light;
        padding-top: 1em;
        background-color: transparentize(white, 0.2);
    }

    .number {
        border: 1px solid $light;
        font-size: 3em;
        width: 1.5em;
        height: 1.5em;
        display: inline-block;
        text-align: center;
    }

    .row {
        margin-bottom: 1em;
    }

    .col {
        text-align: center;
    }

    a {

        transition: background-color 500ms ease;
    }

    a:focus, a:hover {
        background-color: $light;
    }

    .form-control {
        text-align: center;
    }
</style>