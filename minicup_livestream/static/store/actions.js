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
    startHalf(context) {
        context.commit('startTimer');
        context.dispatch('sendObj', {
            action: 'start',
            match: context.state.match.id
        })
    },
    endHalf(context) {
        context.commit('stopTimer');
    },

    goal(context, {player}) {
        context.dispatch('sendObj', {
            action: 'goal',
            match: context.state.match.id,
            player: player,
        });
    },

    sendObj(context, obj) {
        if (context.state.socket.isConnected) {
            this.$socket.sendObj(obj)
        } else {
            context.commit('pushSocketQueue', obj)
        }
    }
}