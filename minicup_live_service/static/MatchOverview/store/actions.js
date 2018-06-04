import Vue from "vue";

export default {
    loadCategories(context) {
        this.commit('setCategories', []);
        return Vue.http.get('/api/category-list').then(response => {
            this.commit('setCategories', response.body.categories);
            this.commit('setMatches', []);
        }, response => {
            // TODO: error
        });
    },
    loadMatches(context, {category}) {
        this.commit('setMatches', []);
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
        window.location.hash = match;
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
    loadMatch({dispatch}, {match}) {
        return Vue.http.get('/api/match/' + match.toString()).then(response => {
            this.commit('setMatch', response.body);
            dispatch('loadTeamInfo', {
                mutation: 'setHomeTeamInfo',
                team: response.body.home_team_id
            }) ;
            dispatch('loadTeamInfo', {
                mutation: 'setAwayTeamInfo',
                team: response.body.away_team_id
            })
        }, response => {
            // TODO: error
        });
    },
    loadTeamInfo({dispatch}, {team, mutation}) {
        return Vue.http.get('/api/team-detail/' + team.toString()).then(response => {
            this.commit(mutation, response.body);
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
            !!response.body.success && window.location.reload(true);
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