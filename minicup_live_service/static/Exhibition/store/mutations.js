import _ from 'lodash'

export default {
    setMatch(state, match) {
        state.match = {...state.match, ...match};
    },
    setScore(state, score) {
        state.match.score = score;
    },
    setState(state, state_) {
        state.match.state = state_;
    },



    pushSocketQueue(state, obj) {
        state.socket.queue.push(obj);
    },

    setLoggedIn(state, loggedIn) {
        state.loggedIn = loggedIn;
    },
    setServerTime(state, serverTime) {
        state.serverTimeOffset = (new Date() / 1000) - serverTime;
    },

    // WS related mutations
    SOCKET_ONOPEN(state, event) {
        state.socket.isConnected = true;
        let toSend = _.uniq(state.socket.queue), obj;
        state.socket.queue = [];

        while (obj = toSend.pop()) {
            this.$socket.sendObj(obj);
        }
    },
    SOCKET_ONCLOSE(state, event) {
        state.socket.isConnected = false;
    },
    SOCKET_ONERROR(state, event) {
        state.socket.isConnected = false;
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE(state, data) {
        state.lastData = data;
        if (_.has(data, 'match')) {
            this.commit('setMatch', data.match);
        }
        if (_.has(data, 'logged')) {
            this.commit('setLoggedIn', data.logged);
        }
        if (_.has(data, 'server_time')) {
            this.commit('setServerTime', data.server_time);
        }
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
        // attempt to reconnect
    },
    SOCKET_RECONNECT_ERROR(state) {
        state.socket.reconnectError = true;
    },
};