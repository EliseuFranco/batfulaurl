<template>
    <section class="flex flex-col h-full w-full">
            <Message :msg="msg"/>
        <div  class="bg-black/60 fixed top-0 left-0 w-full h-dvh z-70 flex items-center justify-center" v-if="openURLModal">
            <div class="bg-black w-full max-w-xl">
                <FormComponent :hideButton="openURLModal" @regist="handlerUrlToRegist"/>
            </div>
        </div>
        <div class="text-white p-10">
                <div class="flex items-center gap-5">
                    <svg @click="sendEvent" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-panel-right-icon lucide-panel-right cursor-pointer"><rect width="18" height="18" x="3" y="3" rx="2"/>
                        <path d="M15 3v18"/></svg>
                    <h1 class="text-xl font-bold md:text-2xl text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-blue-200">URL Analytics Dashboard</h1>
                </div>
                <p>Monitore o desempenho das suas URLs curtas com insights detalhados</p>
        </div>
        <div class="p-10 grow">
            <MetrictsCards :data="header"/>
        </div>
        <div class="w-full md:max-w-3xl p-2">
            <AreaChart />
        </div>
        <div ref="userUrl">
            <UserUrls :urls="all_urls"/>
        </div>
    </section>
</template>


<script setup>
    import { ref, onMounted } from 'vue';
    import MetrictsCards from './MetrictsCards.vue';
    import AreaChart from './AreaChart.vue';
    import UserUrls from './UserUrls.vue';
    import FormComponent from './FormComponent.vue';
    import { eventBus } from '../utils/extensions';
    import Message from './Message.vue';

    import { create_url } from '../utils/api';


    const emit = defineEmits(['close'])
    const openURLModal = ref(false)
    const userUrl = ref('')
    const msg = ref('')
    const all_urls = ref([])
    const header = ref({})

    const sendEvent = function(){
        emit('close')
    }

    const toggleModal = function(data){
        openURLModal.value = !openURLModal.value
    }
    const scrollToUrl = function(){
        if(userUrl.value){
            userUrl.value.scrollIntoView({behavior: 'smooth'})
        }
    }

    const handlerUrlToRegist = async function(url){

        const token = localStorage.getItem('token')
        url.token = token
        const data = await create_url(url)
        
        if(data.error) {
            msg.value = data.error
            return
        }
        console.log(data)
    }

    eventBus.on('open', toggleModal)
    eventBus.on('close', toggleModal)
    eventBus.on('ScrollToUrls', scrollToUrl)

    onMounted(async () => {

         const token = localStorage.getItem('token')
         const resqueToken = await fetch('http://127.0.0.1:8000/dashboard', {
            headers : {
                'Authorization': `Bearer ${token}`
            }
        })

        const tokenData = await resqueToken.json()
        console.log(tokenData)
        all_urls.value = tokenData.all_urls
        header.value = tokenData.header

    })

</script>