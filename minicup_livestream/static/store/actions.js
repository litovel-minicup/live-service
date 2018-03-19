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
    openMatch({dispatch}, d) {
        dispatch('loadMatch', d);
        dispatch('loadEvents', d);
        dispatch('sendObj', {
                action: 'subscribe',
                ...d
            }
        );
    },
    loadMatch(context, {match}) {
        Vue.http.get('/api/match/' + match.toString()).then(response => {
            this.commit('setMatch', response.body);
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
    startHalf({commit}) {
        commit('startTimer');
    },
    endHalf({commit}) {
        commit('stopTimer');
    },

    goal({dispatch, state}, {player}) {
        dispatch('sendObj', {
            action: 'goal',
            match: state.match.id,
            player: player,
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