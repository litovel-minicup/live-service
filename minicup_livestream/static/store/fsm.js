import StateMachine from "state-machine";

const fsm = new StateMachine({
    transitions: [
        'start = s > r1',
        'timer = r1 > h',
        'start = h > r2',
        'timer = r2 > e',
    ],
/*    handlers: {
        '(r1 r2)': function (event, fsm) {
            console.log('In first or second halftime!');
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
    }*/
});

export default fsm;