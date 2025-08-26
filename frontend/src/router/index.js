import {createRouter, createWebHistory} from 'vue-router'
import {jwtDecode} from 'jwt-decode'

import HomeView from '../views/HomeView.vue'
import DashboardView from '../views/DashboardView.vue'
import AuthView from '../views/AuthView.vue'
import Logout from '../components/Logout.vue'


const routes = [

    {
        path: '/',
        component: HomeView
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: DashboardView,
        meta : {
            requiresAuth: true 
        }
    },
    {
        path: '/login',
        name: 'login',
        component: AuthView
    },
    {
        path: '/register',
        name: 'register',
        component: AuthView
    },
    {
        path: '/logout',
        name: 'Logout',
        component: Logout
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
    if(!token) {
        if(to.meta.requiresAuth){
            next({name : 'login', query: {sessExpired: true}})
        } else next()

    } else {
        const { exp } = jwtDecode(token)
        const isAuthenticated = Boolean(exp * 1000 > Date.now())

        if(to.meta.requiresAuth && !isAuthenticated){
            next('/login')
        }
        else {
            next()
        }
    }
})


export default router