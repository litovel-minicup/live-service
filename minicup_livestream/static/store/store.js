import Vuex from 'vuex';
import Vue from "vue";


Vue.use(Vuex);
const store = new Vuex.Store({
    actions: {
        loadCategories(context) {
            Vue.http.get('/api/category-list').then(response => {
                this.commit('setCategories', response.body.categories);
                this.commit('setMatches', []);
            }, response => {
                // TODO: error
            });
        },
        loadMatches(context, {category}) {
            Vue.http.get('/api/category/' + category.toString()).then(response => {
                this.commit('setMatches', response.body.matches);
                this.commit('setMatch', {});
            }, response => {
                // TODO: error
            });
        },
        loadMatch(context, {match}) {
            Vue.http.get('/api/match/' + match.toString()).then(response => {
                this.commit('setMatch', response.body);
            }, response => {
                // TODO: error
            });
        },
    },
    state: {
        lastData: null,
        socket: {
            isConnected: false,
            reconnectError: false
        },

        matches: [],
        categories: [],
        category: null,

        match: {}
    },
    mutations: {
        setCategories(state, cats) {
            state.categories = cats;
        },
        setMatches(state, matches) {
            state.matches = matches
        },
        setCategory(state, id) {
            state.category = id
        },
        setMatch(state, match) {
            state.match = match
        },

        SOCKET_ONOPEN(state, event) {
            state.socket.isConnected = true;

        },
        SOCKET_ONCLOSE(state, event) {
            state.socket.isConnected = false;

        },
        SOCKET_ONERROR(state, event) {
            console.error(state, event)
        },
        // default handler called for all methods
        SOCKET_ONMESSAGE(state, data) {
            state.lastData = data
        },
        // mutations for reconnect methods
        SOCKET_RECONNECT(state, count) {
            console.info(state, count)
        },
        SOCKET_RECONNECT_ERROR(state) {
            state.socket.reconnectError = true;
        },
    },
});


export default store