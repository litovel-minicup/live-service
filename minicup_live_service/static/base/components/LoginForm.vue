<template>
    <form @submit.prevent="send">
        <img src="./../../assets/logo.svg" alt="Logo Litovel MINICUP">
        <h1>{{ title }}</h1>
        <label>
            <input
                    v-model="pin"
                    ref="pin"

                    type="password"
                    pattern="[0-9]*"
                    inputmode="numeric"
                    autofocus
                    class="form-control"
                    placeholder="PIN"
            >
            <input type="submit" class="form-control" value="Přihlásit se">
        </label>
    </form>
</template>

<script>
    export default {
        name: "login-form",
        props: {
            title: {
                type: String,
                default: 'Živé přenosy'
            }
        },
        methods: {
            send() {
                this.$store.dispatch('login', {
                    pin: this.pin,
                }).then(() => {
                    if (!this.$store.state.loggedIn) {
                        this.$toastr.w('Incorrect PIN.');
                        this.pin = '';
                        this.$refs.pin.focus();
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
    }
</script>

<style scoped lang="scss">
    form {
        background-color: #4180ff;
        padding: 3em;
        text-align: center;
        font-variant-caps: all-petite-caps;
        img {
            max-width: 100%;
            margin-bottom: 3em;
        }
        h1 {
            color: white;
            font-size: 1.5em;
        }
        .form-control {
            border-radius: 0;
            text-align: center;
            border: 0;
            &[type=submit] {
                background-color: #ffd800;
                margin-top: 1rem;
                font-variant-caps: all-petite-caps;
                cursor: pointer;
            }
        }
    }
</style>