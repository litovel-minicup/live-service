import _ from 'lodash'

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
    },
    resetMatch(state) {
        state.match.id = 0;
        window.location.hash = '';
    },
    setEvents(state, events) {
        state.events = events;
        this.commit('refreshMatchGoals', 'homeTeamInfo');
        this.commit('refreshMatchGoals', 'awayTeamInfo');
    },
    setHomeTeamInfo(state, homeTeamInfo) {
        state.homeTeamInfo = homeTeamInfo;
        this.commit('refreshMatchGoals', 'homeTeamInfo');
    },
    setAwayTeamInfo(state, awayTeamInfo) {
        state.awayTeamInfo = awayTeamInfo;
        this.commit('refreshMatchGoals', 'awayTeamInfo');
    },
    addEvent(state, event) {
        state.events.unshift(event);

        if (event.type === 'goal' && event.player_id) {
            const found = _.filter(_.concat(
                state.homeTeamInfo.players,
                state.awayTeamInfo.players,
            ), (p) => p.id === event.player_id);
            if (_.isEmpty(found)) return;

            found[0].match_goals++;
            found[0].total_goals++;
        }
    },
    refreshMatchGoals(state, teamProp) {
        let p;
        for (p of state[teamProp].players) {
            p.match_goals = _.size(_.filter(
                state.events,
                (me) => me.type === 'goal' && me.player_id === p.id
            ));
        }

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