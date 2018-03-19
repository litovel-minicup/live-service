<template>
    <div class="spinner">
        <div class="cube" v-if="enable">
            <div class="cube__item--1 cube__item"></div>
            <div class="cube__item--2 cube__item"></div>
            <div class="cube__item--4 cube__item"></div>
            <div class="cube__item--3 cube__item"></div>
        </div>
        <div class="check__wrapper" v-else>
            <svg class="check" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                <circle class="check__circle" cx="26" cy="26" r="25" fill="none"></circle>
                <path class="check__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"></path>
            </svg>
        </div>
    </div>
</template>

<script>
    export default {
        name: "spinner",
        props: {
            enable: {
                type: Boolean,
                default: false,
                required: false,
            }
        },
    }
</script>

<style scoped lang="scss">
    $color: #4180ff;

    .cube {
        margin: 20px auto;
        width: 40px;
        height: 40px;
        position: relative;
        transform: rotateZ(45deg);

        .cube__item {
            float: left;
            width: 50%;
            height: 50%;
            position: relative;
            transform: scale(1.1);
        }

        .cube__item:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: $color;
            animation: cube 2s infinite linear both;
            transform-origin: 100% 100%;
        }

        .cube__item--2 {
            transform: scale(1.1) rotateZ(90deg);
        }

        .cube__item--3 {
            transform: scale(1.1) rotateZ(180deg);
        }

        .cube__item--4 {
            transform: scale(1.1) rotateZ(270deg);
        }

        .cube__item--2:before {
            animation-delay: 0.25s;
        }
        .cube__item--3:before {
            animation-delay: 0.5s;
        }
        .cube__item--4:before {
            animation-delay: 0.75s;
        }
    }

    @keyframes cube {
        0%, 10% {
            transform: perspective(140px) rotateX(-180deg);
            opacity: 0;
        }
        25%, 75% {
            transform: perspective(140px) rotateX(0deg);
            opacity: 1;
        }
        90%, 100% {
            transform: perspective(140px) rotateY(180deg);
            opacity: 0;
        }
    }

    .check__wrapper {
        $curve: cubic-bezier(0.650, 0.000, 0.450, 1.000);

        .check__circle {
            stroke-dasharray: 166;
            stroke-dashoffset: 166;
            stroke-width: 2;
            stroke-miterlimit: 10;
            stroke: $color;
            fill: none;
            animation: stroke .6s $curve forwards;
        }

        .check {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            display: block;
            stroke-width: 2;
            stroke: #fff;
            stroke-miterlimit: 10;
            margin: 10% auto;
            box-shadow: inset 0 0 0 $color;
            animation: fill .4s ease-in-out .4s forwards,
            scale .3s ease-in-out .9s forwards,
            fade 1s ease-in-out 1s forwards;
        }

        .check__check {
            transform-origin: 50% 50%;
            stroke-dasharray: 48;
            stroke-dashoffset: 48;
            animation: stroke .3s $curve .8s forwards;
        }

        @keyframes stroke {
            100% {
                stroke-dashoffset: 0;
            }
        }

        @keyframes scale {
            0%, 100% {
                transform: none;
            }
            50% {
                transform: scale3d(1.1, 1.1, 1);
            }
        }

        @keyframes fill {
            100% {
                box-shadow: inset 0 0 0 30px $color;
            }
        }

        @keyframes fade {
            0% {
                opacity: 1;
            }
            100% {
                opacity: 0;
            }
        }
    }
</style>