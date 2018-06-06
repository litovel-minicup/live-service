import Vue from "vue";

export default {

    addHomeGoal({commit, dispatch}) {
        commit('setScore', [
            Number(this.state.match.score[0]) + 1,
            Number(this.state.match.score[1]),
        ]);
        dispatch('submitMatch');
    },
    addAwayGoal({commit, dispatch}) {
        commit('setScore', [
            Number(this.state.match.score[0]),
            Number(this.state.match.score[1]) + 1,
        ]);
        dispatch('submitMatch');
    },
    submitMatch({dispatch}) {
        dispatch('sendObj', {
            match_obj: this.state.match
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

    sendObj({state, commit}, obj) {
        if (state.socket.isConnected) {
            this.$socket.sendObj(obj)
        } else {
            commit('pushSocketQueue', obj)
        }
    }
}