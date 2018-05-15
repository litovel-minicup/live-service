import VueRouter from "vue-router";


import MatchList from './components/MatchList'
import CategoryList from './components/CategoryList'
import MatchDetail from './components/MatchDetail'


const routes = [
    {path: '/', component: CategoryList, name: 'home'},
    {path: '/category/:category', component: MatchList, name: 'category'},
    {path: '/match/:match', component: MatchDetail, name: 'match'},
];
const router = new VueRouter({routes});

export default router