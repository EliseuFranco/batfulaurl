<template>
    <section class="flex flex-col min-h-screen w-full overflow-hidden">
            <Message :msg="msg"/>
        <div  class="bg-black/60 fixed top-0 left-0 w-full h-dvh z-70 flex items-center justify-center" v-if="openURLModal">
            <div class="bg-black w-full max-w-xl">
                <FormComponent :hideButton="openURLModal" @regist="handlerUrlToRegist" @update="listUserURL" @close="openURLModal = false"/>
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
        <div class="p-3 grow">
            <MetrictsCards :data="header"/>
        </div>
        <div class="flex flex-col lg:flex-row items-center lg:p-5">
            <AreaChart :chartData="areaChartData" :chartData2 ="areaData2" class="w-full"/>
            <BarChart class=""/>
        </div>
        <div class="flex flex-col lg:flex-row ">
            <DonutsChart :data="devices"/>
            <CityTable class="grow" :data="cities"/>
        </div>
        <div ref="userUrl">
            <UserUrls :urls="all_urls" @page="handlerPage" :pages="pageInfo" @message="handlerCopyMessage"/>
        </div>
    </section>
</template>


<script setup>
    import { ref, onMounted } from 'vue';
    import MetrictsCards from './MetrictsCards.vue';
    import AreaChart from './AreaChart.vue';
    import UserUrls from './UserUrls.vue';
    import FormComponent from './FormComponent.vue';
    import { eventBus, calcConversionRate } from '../utils/extensions';
    import Message from './Message.vue';
    import { create_url, getUserData } from '../utils/api';
    import BarChart from './BarChart.vue';
    import DonutsChart from './Donuts.chart.vue';
    import CityTable from './CityTable.vue';
    

    const emit = defineEmits(['close'])

    const openURLModal = ref(false)
    const userUrl = ref('')
    const msg = ref('')
    const all_urls = ref([])
    const header = ref({})
    const currantPage = ref(1)
    const areaChartData = ref([])
    const areaData2 = ref([])
    const devices = ref([])
    const cities = ref([])
     const pageInfo = ref()

    
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
        await listUserURL()
        console.log('URL criada: ', data)
    }

    const handlerPage = async function(page){
        const data = await getUserData(page)
        all_urls.value = data.all_urls
        
    }

    eventBus.on('open', toggleModal)
    eventBus.on('close', toggleModal)
    eventBus.on('ScrollToUrls', scrollToUrl)

    const listUserURL = async function() {
        const token = localStorage.getItem('token')
        const apiUrl = import.meta.env.VITE_API_URL

        const resquetToken = await fetch(`${apiUrl}/dashboard?page=${currantPage.value}`, {
            headers : { 'Authorization': `Bearer ${token}` }
        })

        const tokenData = await resquetToken.json()

        if(tokenData.error){
            msg.value = "Não foi pssível realizar login, erro na comunicação com o servidor"
            return
        }

        all_urls.value = tokenData.all_urls || {}
        header.value = tokenData.header || {}
        areaChartData.value = tokenData.all_urls.seven_days_clicks || []
        areaData2.value = tokenData.all_urls.unique_7d_clicks || []
        devices.value = tokenData.all_urls.devices || []
        cities.value = tokenData.all_urls.cities || []


        // pageInfo.value = {
        //     page: tokenData.all_urls.page,
        //     total_pages: tokenData.all_urls.total_pages
        // }

        // all_urls.value.at(0).page = tokenData.all_urls.page
        // all_urls.value.at(0).total_pages = tokenData.all_urls.page
        
    }

    const handlerCopyMessage = function(message){
        msg.value = message;
        console.log(message)

        setTimeout(()=> {
            msg.value = ''
        }, 1500)
    }


    onMounted(async () => listUserURL())
   

</script>