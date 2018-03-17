import Vue from 'vue'
import VueRouter from 'vue-router'
import VueNativeSock from 'vue-native-websocket'
import BootstrapVue from 'bootstrap-vue'
import {sync} from 'vuex-router-sync'
import VueResource from 'vue-resource'


import App from './App.vue'
import router from './router'

import store from './store/store'


Vue.use(VueNativeSock, 'ws://localhost:8888/ws/broadcast', {
    reconnection: false,
    format: 'json',
    store
});
Vue.use(VueResource);
Vue.use(BootstrapVue);
Vue.use(VueRouter);
sync(store, router);


const app = new Vue({
    el: '#app',
    store,
    router,
    render: h => h(App)
});


