import camelCaseKeys from 'camelcase-keys'

export default {
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
        state.match = {...state.match, ...match};
        if (state.fsm.state !== state.match.state)
            this.commit('goToFsmState', state.match.state);
    },
    setEvents(state, events) {
        state.events = events
    },
    addEvent(state, event) {
        state.events.unshift(event)
    },
    startTimer(state) {
        this.commit('doFsmAction', 'start');
    },
    stopTimer(state) {
        this.commit('doFsmAction', 'timer');
    },
    doFsmAction(state, action) {
        state.fsm.do(action);
    },
    goToFsmState(state, fsmState) {
        state.fsm.go(fsmState, true); // force go
    },


    pushSocketQueue(state, obj) {
        state.socket.queue.push(obj);
    },

    connectFsmEvent(state, {event, cb}) {
        state.fsm.on(event, (...args) => {
            cb(...args)
        });
    },

    setLoggedIn(state, loggedIn) {
        state.loggedIn = loggedIn;
    },
    setFsmStateChangeListenerRegistered(state) {
        state.fsmStateChangeListenerRegistered = true;
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
        data = camelCaseKeys(data);
        state.lastData = data;
        if (_.has(data, 'event')) {
            this.commit('addEvent', data.event);
        }
        if (_.has(data, 'events')) {
            this.commit('setEvents', data.events);
        }
        if (_.has(data, 'match')) {
            this.commit('setMatch', data.match);
        }
        if (_.has(data, 'logged')) {
            this.commit('setLoggedIn', data.logged);
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