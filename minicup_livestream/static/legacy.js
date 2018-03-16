Number.prototype.pad = function (size) {
    let sign = Math.sign(this) === -1 ? '-' : '';
    return sign + new Array(size).concat([Math.abs(this)]).join('0').slice(-size);


};


function initialize(matchId) {
    var app = new Vue({
        el: '#vue-app',
        data: {
            score: [null, null],
            events: [],
            time: null,
            halfStart: null,
            halfIndex: null,
            playing: false,
            matchEnd: false
        },
        methods: {
            refreshScore: function () {
                axios.get(
                    '/online/api/state/' + matchId.toString()
                ).then(function (response) {
                    app.score = response.data.score;
                    app.halfIndex = response.data.halfIndex;
                    app.halfStart = response.data.halfStart;
                }).catch(function (error) {
                    console.log(error);
                });
            },
            refreshEvents: function () {
                axios.get(
                    '/online/api/events/' + matchId.toString()
                ).then(function (response) {
                    app.events = response.data.events;
                }).catch(function (error) {
                    console.log(error);
                });

            },
            refreshTime: function () {
                var secsFromStart = ((new Date() - new Date(1000 * this.halfStart)) / 1000);
                // console.log(this.halfIndex);
                // console.log(secsFromStart);
                if (secsFromStart < 10 * 60) {
                    this.time = new Date(secsFromStart * 1000);
                    this.playing = true;
                } else {
                    this.time = null;
                    this.playing = false;
                }

            },
            startHalf: function () {
                axios.post(
                    '/online/api/start-half/' + matchId.toString()
                ).then(function (response) {
                    app.refreshScore();
                    app.refreshTime();
                }).catch(function (error) {
                    console.log(error);
                });
            },
            goal: function (playerId) {
                axios.post(
                    '/online/api/goal/' + matchId.toString(),
                    {
                        playerId: playerId
                    }
                ).then(function (response) {
                    app.refreshScore();
                    app.refreshEvents();
                    $('.modal').modal('hide');
                }).catch(function (error) {
                    console.log(error);
                });
            }
        },
        computed: {
            timeFormatted: function () {
                if (!this.time) return '00:00';
                return this.time.getMinutes().pad(2) + ':' + this.time.getSeconds().pad(2);
            }
        },
        beforeMount: function () {
            this.refreshScore();
            this.refreshEvents();
            this.refreshTime();
            setInterval(function () {
                app.refreshTime();
            }, 500);
            setInterval(function () {
                app.refreshScore();
                app.refreshEvents();
            }, 2500);
        }
    });


    Vue.filter('default', function (value, default_) {
        return (value == null || value === undefined) ? default_ : value;
    });
    Vue.filter('prettyTime', function (secs) {
        return Math.floor(secs / 60).pad(2) + ':' + (secs % 60).pad(2);
    });
    return app;
}