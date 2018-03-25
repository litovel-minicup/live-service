import StateMachine from "state-machine";

const fsm = new StateMachine({
    transitions: [
        // service actions used for loading from server
        'load_init = null > init',
        'load_half_first = null > half_first',
        'load_pause = null > pause',
        'load_half_second = null > half_second',
        'load_end = null > end',

        // standard actions
        'start = init > half_first',
        'timer = half_first > pause',
        'start = pause > half_second',
        'timer = half_second > end',
    ],
    handlers: {
        /*
        ':enter': function (event, fsm) {
            console.log('enter', arguments);
        },
        '@start': function (event, fsm) {
            console.log('Start timer!');
            setTimeout(function () {
                console.log(this);
                console.log(event);
                console.log(fsm);
            }, 1000)
        },
        '@timer': function (event, fsm) {
            console.log('Stop timer!');
        },
        */
    }
});

export default fsm;