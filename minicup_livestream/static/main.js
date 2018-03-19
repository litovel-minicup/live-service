import Vue from 'vue'
import VueRouter from 'vue-router'
import VueNativeSock from 'vue-native-websocket'
import BootstrapVue from 'bootstrap-vue'
import {sync} from 'vuex-router-sync'
import VueResource from 'vue-resource'


import App from './App.vue'
import router from './router'
import store from './store/store'

function createWebSocket(path) {
    const protocolPrefix = (window.location.protocol === 'https:') ? 'wss:' : 'ws:';
    return protocolPrefix + '//' + location.host + path;
}

Vue.use(VueNativeSock, createWebSocket('/ws/broadcast'), {
    reconnection: true,
    format: 'json',
    store
});
Vue.use(VueResource);
Vue.use(BootstrapVue);
Vue.use(VueRouter);
sync(store, router);

Number.prototype.pad = function (size, char='0') {
    let sign = Math.sign(this) === -1 ? '-' : '';
    return sign + new Array(size).concat([Math.abs(this)]).join(char).slice(-size);
};

const app = new Vue({
    el: '#app',
    store,
    router,
    render: h => h(App)
});


