import {createRouter, createWebHistory} from 'vue-router'
import {jwtDecode} from 'jwt-decode'

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
        component: DashboardView,
        meta : {
            requiresAuth: true 
        }
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

router.beforeEach((to, from, next) => {

    const token = localStorage.getItem('token')
    const { exp } = jwtDecode(token)

    const isAuthenticated = Boolean(exp * 1000 > Date.now())

    if(to.meta.requiresAuth && !isAuthenticated){
        next('/login')
    }
    else {
        next()
    }
})


export default router