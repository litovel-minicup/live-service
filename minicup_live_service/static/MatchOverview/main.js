import Vue from './../base/base'
import VueNativeSock from 'vue-native-websocket'
import BootstrapVue from 'bootstrap-vue'
import VueResource from 'vue-resource'
import Raven from 'raven-js';
import RavenVue from 'raven-js/plugins/vue';
import Toastr from 'vue-toastr';
import App from './App.vue'
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
Vue.use(Toastr);


Number.prototype.pad = function (size, char = '0') {
    let sign = Math.sign(this) === -1 ? '-' : '';
    return sign + new Array(size).concat([Math.abs(this)]).join(char).slice(-size);
};


const app = new Vue({
    el: '#app',
    store,
    render: h => h(App),
});



