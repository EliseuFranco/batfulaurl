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
                  <FormComponent @regist="handlerURL"/>
              </div>
              <div class="border border-zinc-900 rounded-xl p-5" v-if="url_created">
                <div class="flex items-center justify-between gap-10 mb-4">
                  <p><span class="font-semibold mb-5">URL curta</span>: {{ url_created.shortned }}</p>
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="lucide lucide-copy-icon lucide-copy text-purple-500 cursor-pointer" @click="handlerClipBoardMSG(url_created.shortned)"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
                    <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                </div>
                <p><span class="font-semibold">URL original</span>: {{ createMask(url_created.original) }}</p>
              </div>
         </div>
         <div>
              <Metrics @metrics="handerMetricErrors" :refresh="refrehMetrics"/>
              <Resources />
         </div>
         <div>
          <Call />
         </div>
          <div ref="faqs">
            <FAQ />
          </div>
          
    </section>
</template>



<script setup>

    import { ref, onMounted, watch} from 'vue'
    import FormComponent from './FormComponent.vue';
    import Message from './Message.vue';
    import Metrics from './Metrics.vue';
    import FAQ from './FAQ.vue';
    import Resources from './Resources.vue';
    import { eventBus, createMask, copyToClipBoard } from '../utils/extensions';
    import Call from './Call.vue';
    import {create_url} from '../utils/api.js'


    const msg = ref('')
    const faqs = ref('')
    const url_created = ref('')
    const refrehMetrics = ref(0)

   
    const clearMessage = function(){
      msg.value = ''
    }

    const handlerURL = async function(data) {
      
      try {
        const token = localStorage.getItem('token')
        data.token = token
        const responseData = await create_url(data)

        if(!responseData.shortened_url){
            msg.value = 'Não foi possível estabelecer ligação com o servidor'
            return
        }
        url_created.value = {shortned: responseData.shortened_url, original: responseData.original_url}
        msg.value = responseData.msg
        refrehMetrics.value++;

      } catch (error) {
        msg.value = 'Houve um erro ao estabelecer ligação'
          console.log('Houve um erro ao criar URL: ', error)
      }
    }

    const handlerClipBoardMSG = async function(text) {
        const message = await copyToClipBoard(text)
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


</script>
