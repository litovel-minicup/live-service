import Vue from 'vue'
import VueRouter from 'vue-router'
import VueNativeSock from 'vue-native-websocket'
import BootstrapVue from 'bootstrap-vue'
import {sync} from 'vuex-router-sync'
import VueResource from 'vue-resource'
import Raven from 'raven-js';
import RavenVue from 'raven-js/plugins/vue';


import App from './App.vue'
import router from './router'
import store from './store/store'

Raven
    .config('https://426ce166aa3646f591835476dcc0b487@sentry.io/306681')
    .addPlugin(RavenVue, Vue)
    .install();

function createWebSocket(path) {
    const protocolPrefix = (window.location.protocol === 'https:') ? 'wss:' : 'ws:';
    return protocolPrefix + '//' + location.host + path;
}


Vue.use(VueNativeSock, createWebSocket('/ws/broadcast'), {
    reconnection: true,
    format: 'json',
    store
});
store.$socket = Vue.prototype.$socket;

Vue.use(VueResource);
Vue.use(BootstrapVue);
Vue.use(VueRouter);
sync(store, router);

Number.prototype.pad = function (size, char = '0') {
    let sign = Math.sign(this) === -1 ? '-' : '';
    return sign + new Array(size).concat([Math.abs(this)]).join(char).slice(-size);
};

Vue.config.errorHandler = function (err, vm, info) {
  // handle error
  // `info` is a Vue-specific error info, e.g. which lifecycle hook
  // the error was found in. Only available in 2.2.0+
    alert();
};

const app = new Vue({
    el: '#app',
    store,
    router,
    render: h => h(App),
});



