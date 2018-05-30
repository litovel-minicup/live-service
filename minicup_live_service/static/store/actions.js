import Vue from "vue";

export default {
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
    openMatch({dispatch}, match = this.state.match.id) {
        dispatch('loadMatch', {match});
        dispatch('loadEvents', {match});
        dispatch('subscribeMatch', {match});
    },
    subscribeMatch({dispatch}, {match}) {
        dispatch('sendObj', {
                action: 'subscribe',
                match
            }
        );
    },
    unsubscribeMatch({dispatch}, {match}) {
        dispatch('sendObj', {
                action: 'unsubscribe',
                match
            }
        );
    },
    loadMatch(context, {match}) {
        return Vue.http.get('/api/match/' + match.toString()).then(response => {
            this.commit('setMatch', response.body);
            this.commit('goToFsmState', response.body.state);
        }, response => {
            // TODO: error
        });
    },
    loadEvents(context, {match}) {
        return Vue.http.get('/api/match-events/' + match.toString()).then(response => {
            context.commit('setEvents', response.body.events);
        }, response => {
            // TODO: error
        });
    },
    login({commit}, {pin}) {
        return Vue.http.post('/api/login', {pin}).then(response => {
            commit('setLoggedIn', !!response.body.success);
        }, response => {
            console.error('Login failed.')
        });
    },
    logout({commit}) {
        return Vue.http.post('/api/logout').then(response => {
            commit('setLoggedIn', false);
        }, response => {
            console.error('Logout failed.')
        });
    },
    startHalf({commit}) {
        commit('startTimer');
    },
    endHalf({commit}) {
        commit('stopTimer');
    },

    goal({dispatch, state}, {player, team}) {
        dispatch('sendObj', {
            action: 'goal',
            match: state.match.id,
            player,
            team,
        });
    },
    deleteEvent({dispatch, state}, event) {
        dispatch('sendObj', {
            action: 'delete_event',
            match: state.match.id,
            event: event.id,
        });
    },
    sendObj({state, commit}, obj) {
        if (state.socket.isConnected) {
            this.$socket.sendObj(obj)
        } else {
            commit('pushSocketQueue', obj)
        }
    }
}