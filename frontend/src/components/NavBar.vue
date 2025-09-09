<template>
       <section class="">
           <nav v-if="$route.fullPath === '/'" class="text-zinc-500 text-sm rounded-2xl p-5">
                <div class="flex flex-wrap flex-row items-center flex-wrap justify-between  gap-3 p-5 md:justify-center font-semibold bg-zinc-900 rounded-2xl">
                    <div class="">
                        <h1 class="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-blue-200 text-xl font-bold">BatfulaURL</h1>
                    </div>
                     <div class="flex flex-col gap-1 md:hidden cursor-pointer" @click="open">
                            <div class="w-5 p-[1px] bg-white"></div>
                            <div class="w-5 p-[1px] bg-white"></div>
                            <div class="w-5 p-[1px] bg-white"></div>
                    </div>
                    <div class="flex flex-col md:flex-row justify-start w-full md:w-auto gap-2 md:items-center" 
                    :class="{'hidden': isMobile , 'showmenu': !isMobile}">
                        <div>
                            <button class="cursor-pointer p-2 bg-blue-" @click="scrollToFaq">FAQ's</button>
                        </div>
                        <div v-if="!isAuthenticated()" class="flex flex-col md:flex-row">
                            <router-link to="/login" class="cursor-pointer p-2">Iniciar sessão</router-link>
                            <router-link to="/register" class="cursor-pointer p-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-blue-200 font-bold">Criar conta</router-link>
                        </div>
                        <div v-else>
                            <router-link to="/dashboard" class="cursor-pointer p-2 vg-" active-class="bg-purple-800">Dashboard</router-link>
                        </div>
                       
                    </div>
                
                </div>
            </nav>
            <router-view></router-view>
       </section>
</template>


<script setup> 

    import { ref, onMounted, onBeforeMount } from 'vue';
    import { eventBus } from '../utils/extensions';
    import { isAuthenticated } from '../utils/extensions';

    const isMobile = ref(window.innerWidth <= 768);

    const scrollToFaq = function(){
        eventBus.emit('scroll')
    }

    const getWindowWidth = function(){
        if(window.innerWidth <= 768){
            isMobile.value = true
        } else {
            isMobile.value = false
        }
    }

    onMounted(() => {
        getWindowWidth()
        window.addEventListener('resize', getWindowWidth)
    })

    onBeforeMount(()=>{
        window.removeEventListener('resize', getWindowWidth)
    })

    const open = function(){
        isMobile.value = !isMobile.value
    }


</script>

<style scoped>

    @keyframes show {
        from {opacity: 0;}
        to{opacity: 1;}

    }
    .showmenu{
        animation: show 0.5s ease-in-out;
    }
    
    @media (min-width: 768px) {
    .showmenu {
        animation: none !important;
    }
    }


</style>