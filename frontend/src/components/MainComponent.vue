<template>

    <section class="">
       <div>
            <Message :msg="msg" />
       </div>
          <div class="p-10 text-white flex flex-col justify-center gap-7 items-center">
            <div class="bg-gradient-to-r from-purple-600 to-fuchsia-800 p-5 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              class="lucide lucide-link2-icon lucide-link-2"><path d="M9 17H7A5 5 0 0 1 7 7h2"/>
                <path d="M15 7h2a5 5 0 1 1 0 10h-2"/><line x1="8" x2="16" y1="12" y2="12"/></svg>
            </div>
            <div class="flex flex-col justify-center items-center gap-3">
              <h1 class="text-purple-600 text-3xl font-bold">Encurtador de <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-800 to-blue-200">URLS</span></h1>
              <div class="">
                <p class="w-ful max-w-4xl text-sm sm:text-xl text-center text-zinc-500">
                  Transforme URLs longas em links curtos e elegantes. Monitore cliques e gerencie seus links facilmente</p>
              </div>
            </div>
              <div>
                  <FormComponent @regist="handlerURL" @update="listURLS"/>
              </div>
              <div>
                  <ListUrls :all_url="URLS" @msg="handlerClipBoardMSG"/>
            </div>
         </div>
         <div>
              <Metrics :refresh="refreshMetrics" @metrics="handerMetricErrors" @update="listURLS" />
              <Resources />
            </div>
            <div ref="faqs">
              <FAQ />
            </div>
          
    </section>
</template>



<script setup>

    import { ref, onMounted, watch} from 'vue'
    import FormComponent from './FormComponent.vue';
    import ListUrls from './ListUrls.vue';
    import Message from './Message.vue';
    import Metrics from './Metrics.vue';
    import FAQ from './FAQ.vue';
    import Resources from './Resources.vue';
import { eventBus } from '../utils/extensions';


    const msg = ref('')
    const refreshMetrics = ref(0)
    const URLS = ref([])
    const faqs = ref('')

    const listURLS = function(){
      URLS.value = JSON.parse(localStorage.getItem('urls') || '[]')
  
    }

    const clearMessage = function(){
      msg.value = ''
    }

    const handlerURL = async function(data) {

      data.user_id = null
      
      try {
        const request = await fetch('http://127.0.0.1:8000/create_shorten_url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify(data)
        });

        if(!request.ok){
          console.log("Algo correu mal")
          console.log(request)
            msg.value = 'Não foi possível estabelecer ligação com o servidor'
        }

        const responseData  = await request.json();
        console.log(responseData)


        if (responseData.shorten_url){
          console.log('Já existe essa url')
          msg.value = responseData.msg
          return
        }

        const storedUrls = JSON.parse(localStorage.getItem('urls') || '[]')
        console.log(responseData)
     
        storedUrls.push({'shortened_url': responseData .shortened_url, original_url: responseData.original_url})
        localStorage.setItem('urls',JSON.stringify(storedUrls))
        msg.value = responseData.msg
        refreshMetrics.value ++
        listURLS()

      } catch (error) {
        msg.value = 'Houve um erro ao estabelecer ligação'
          console.log('Houve um erro ao criar URL: ', error)
      }
    }

    const handlerClipBoardMSG = function(message) {
        msg.value = message
    }

    watch(msg, (newMsg) => {
      if(newMsg){
        setTimeout(clearMessage, 3000)
      }
    })

    const handerMetricErrors = function(error){
        msg.value = error
    }

    const scrollTofaq = function(){
      if(faqs.value){
        faqs.value.scrollIntoView({behavior: 'smooth'})
      }
    }

    eventBus.on('scroll',scrollTofaq)


    onMounted(async () => listURLS())


</script>
