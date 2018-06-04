import Vue from "vue";
import VueLoading from "vue-loading-template";


Vue.filter("onlineStateName", state => {
    return {
        'init': 'před zápasem',
        'half_first': '1. poločas',
        'pause': 'přestávka',
        'half_second': '2. poločas',
        'end': 'po zápase'
    }[state];
});

Vue.filter("score", val => {
    return val === null ? '-' : val;
});


Vue.component('v-loading', {
    template: '<vue-loading type="spin" color="#0e5eff" :size="{ width: \'100px\', height: \'100px\' }"></vue-loading>',
    components: {VueLoading}
});

export default Vue;