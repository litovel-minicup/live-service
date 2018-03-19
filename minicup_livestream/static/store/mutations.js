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
        state.match = _.merge({}, state.match, match);
    },
    setEvents(state, events) {
        state.events = events
    },
    addEvent(state, event) {
        state.events.unshift(event)
    },

    startTimer(state) {
        state.fsm.do('start');
    },
    connectFsmEvent(state, {event, cb}) {
        state.fsm.on(event, (...args) => {
            cb(...args)
        });
    },
    stopTimer(state) {
        state.fsm.do('timer');
    },
    pushSocketQueue(state, obj) {
        state.socket.queue.push(obj);
    },

    SOCKET_ONOPEN(state, event) {
        state.socket.isConnected = true;
        let obj;
        while (obj = state.socket.queue.pop()) {
            this.$socket.sendObj(obj);
        }
    },
    SOCKET_ONCLOSE(state, event) {
        state.socket.isConnected = false;
    },
    SOCKET_ONERROR(state, event) {
        console.error(state, event)
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE(state, data) {
        state.lastData = data;
        console.log('Message: ', data);
        this.commit('addEvent', data.event);
        this.commit('setMatch', data.match);
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
        // console.info(state, count)
    },
    SOCKET_RECONNECT_ERROR(state) {
        state.socket.reconnectError = true;
    },
};