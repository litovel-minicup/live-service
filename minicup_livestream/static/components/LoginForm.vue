<template>
    <div class="login-form" @click="click">
        <div class="row mb-2 justify-content-center">
            <div class="col-4">
                <label>
                    <input type="password" v-model="pin" class="form-control">
                </label>
            </div>
        </div>
        <div class="row">
            <div class="col"><a class="number">1</a></div>
            <div class="col"><a class="number">2</a></div>
            <div class="col"><a class="number">3</a></div>
        </div>
        <div class="row">
            <div class="col"><a class="number">4</a></div>
            <div class="col"><a class="number">5</a></div>
            <div class="col"><a class="number">6</a></div>
        </div>
        <div class="row">
            <div class="col"><a class="number">7</a></div>
            <div class="col"><a class="number">8</a></div>
            <div class="col"><a class="number">9</a></div>
        </div>
        <div class="row">
            <div class="col"><a class="number" @click="send">#</a></div>
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
                    xsrf: this.$cookie.get('_xsrf')
                }).then(() => {
                    if (!this.$store.state.loggedIn) {
                        this.$toastr.w('Incorrect PIN.');
                        this.pin = '';
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