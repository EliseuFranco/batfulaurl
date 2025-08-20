import {createRouter, createWebHistory} from 'vue-router'

import HomeView from '../views/HomeView.vue'
import DashboardView from '../views/DashboardView.vue'
import AuthView from '../views/AuthView.vue'


const routes = [

    {
        path: '/',
        component: HomeView
    },
    {
        path: '/dashboard',
        component: DashboardView
    },
    {
        path: '/login',
        component: AuthView
    },
    {
        path: '/register',
        component: AuthView
    },

]

const router = createRouter(
    {
        history: createWebHistory(),
        routes

    }
)


export default router