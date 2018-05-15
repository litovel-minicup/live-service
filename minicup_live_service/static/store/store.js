import Vuex from 'vuex';
import Vue from "vue";
import {StateHelper} from 'state-machine'
import fsm from './fsm'
import actions from './actions'
import mutations from './mutations'

Vue.use(Vuex);
const store = new Vuex.Store({
    state: {
        lastData: null,
        socket: {
            isConnected: false,
            reconnectError: false,
            queue: []
        },

        matches: [],
        categories: [],
        category: null,

        match: {
            score: [0, 0],
        },
        events: [],

        fsm: fsm,

        loggedIn: false
    },
    actions,
    mutations,
    strict: true

});


export default store