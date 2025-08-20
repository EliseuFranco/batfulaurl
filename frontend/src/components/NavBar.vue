<template>
       <section class="">
           <nav v-if="$route.fullPath === '/'" class="text-white text-sm rounded-2xl p-5">
                <div class="flex items-center gap-3 p-5 justify-center font-semibold bg-zinc-900 rounded-2xl">
                    <router-link to="/dashboard" class="cursor-pointer p-2 vg-" active-class="bg-purple-800">Dashboard</router-link>
                    <router-link to="/login" class="cursor-pointer p-2">Iniciar sessão</router-link>
                    <router-link to="/register" class="cursor-pointer p-2">Registar</router-link>
                    <button class="cursor-pointer p-2" @click="scrollToFaq">FAQ's</button>
                </div>
            </nav>
            <router-view></router-view>
       </section>
</template>


<script setup> 

    import { eventBus } from '../utils/extensions';

    const scrollToFaq = function(){
        eventBus.emit('scroll')
    }
</script>