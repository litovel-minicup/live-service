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
    openMatch({dispatch}, data) {
        dispatch('loadMatch', data);
        dispatch('loadEvents', data);
        dispatch('sendObj', {
                action: 'subscribe',
                ...data
            }
        );
    },
    loadMatch(context, {match}) {
        Vue.http.get('/api/match/' + match.toString()).then(response => {
            this.commit('setMatch', response.body);
            this.commit('doFsmAction', 'load_' + response.body.state);
        }, response => {
            // TODO: error
        });
    },
    loadEvents(context, {match}) {
        Vue.http.get('/api/match-events/' + match.toString()).then(response => {
            context.commit('setEvents', response.body.events);
        }, response => {
            // TODO: error
        });
    },
    login({commit}, {pin, xsrf}) {
        return Vue.http.post('/api/login?_xsrf=' + xsrf.toString(), {pin}).then(response => {
            console.log(response.body);
            commit('setLoggedIn', !!response.body.success);
        }, response => {
            console.error('Login failed.')
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
        console.log(event);
    },
    sendObj({state, commit}, obj) {
        if (state.socket.isConnected) {
            this.$socket.sendObj(obj)
        } else {
            commit('pushSocketQueue', obj)
        }
    }
}