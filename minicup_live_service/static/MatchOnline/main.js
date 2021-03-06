import Vue from './../base/base'
import VueRouter from 'vue-router'
import VueNativeSock from 'vue-native-websocket'
import BootstrapVue from 'bootstrap-vue'
import {sync} from 'vuex-router-sync'
import VueLoading from 'vue-loading-template'
import VueResource from 'vue-resource'
import Raven from 'raven-js';
import RavenVue from 'raven-js/plugins/vue';
import Toastr from 'vue-toastr';
import App from './App.vue'
import router from './router'
import store from './store/store'


require('vue-toastr/src/vue-toastr.scss');

Raven.config(
    'https://426ce166aa3646f591835476dcc0b487@sentry.io/306681',
    {
        ignoreUrls: [new RegExp('localhost:.*'), new RegExp('127\..*')]
    }
).addPlugin(RavenVue, Vue).install();

function createWebSocket(path) {
    const protocolPrefix = (window.location.protocol === 'https:') ? 'wss:' : 'ws:';
    return `${protocolPrefix}//${location.host}${path}`;
}


Vue.use(VueNativeSock, createWebSocket('/ws/live'), {
    reconnection: true,
    format: 'json',
    store
});
store.$socket = Vue.prototype.$socket;

Vue.use(VueResource);
Vue.use(BootstrapVue);
Vue.use(VueRouter);
Vue.use(Toastr);

sync(store, router);

Number.prototype.pad = function (size, char = '0') {
    let sign = Math.sign(this) === -1 ? '-' : '';
    return sign + new Array(size).concat([Math.abs(this)]).join(char).slice(-size);
};

Vue.filter("onlineStateName", state => {
    return {
        'init': 'před zápasem',
        'half_first': '1. poločas',
        'pause': 'přestávka',
        'half_second': '2. poločas',
        'end': 'po zápase'
    }[state];
});


Vue.component('v-loading', {
    template: '<vue-loading type="spin" color="#0e5eff" :size="{ width: \'100px\', height: \'100px\' }"></vue-loading>',
    components: {VueLoading}
});

const app = new Vue({
    el: '#app',
    store,
    router,
    render: h => h(App),
});



