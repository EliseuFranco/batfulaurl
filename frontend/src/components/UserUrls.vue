<template>
  <section class="p-10 mx-auto">
    <h2 class="text-xl text-zinc-100 font-semibold mb-4">URLs Encurtadas</h2>

    <div v-if="urls.length > 0 ">
      <ul class="space-y-4">
        <li
          v-for="(url, index) in urls"
          :key="index"
          class="bg-zinc-950 rounded-xl w-full p-4 shadow flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 text-sm">
          <div class="w-full space-y-4">
            <div class="flex items-center justify-between w-full ">
                <div class="w-full">
                    <p class="text-zinc-300 text-sm">Original:</p>
                    <a :href="url.original_url" target="_blank" class="text-blue-400 break-all hover:underline">
                      {{ createMask(url.original_url) }}
                    </a>
                    <p class="text-zinc-300 mt-2 text-sm">Encurtada:</p>
                      <a :href="`${apiUrl}/redirect?user_slug=` + url.slug" target="_blank" class="text-purple-500 break-all hover:underline">
                      {{ url.shortened_url }}
                      </a>
                </div>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round"
                 class="lucide lucide-copy-icon lucide-copy cursor-pointer" @click="copyToClipBoard(url.shortened_url)">
                  <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
                  <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
            </div>
            <div class="flex flex-col gap-2 md:flex-row justify-between">
              <div>
                  <p class="text-zinc-400">Total clicks</p>
                  <span>{{ url.total_clicks }}</span>
              </div>
              <div>
                  <p class="text-zinc-400">Únicos</p>
                  <span>{{ url.unique_clicks }}</span>
              </div>
              <div>
                  <p class="text-zinc-400">Taxa de conversão</p>
                  <span>{{ calcConversionRate(url.unique_clicks, url.total_clicks) }} %</span>
              </div>
              <div>
                  <p class="text-zinc-400">Criado em</p>
                  <span>{{ url.data }}</span>
              </div>
              <div>
                  <p class="text-zinc-400">Ação</p>
                  <span class="text-red-400 underline cursor-pointer" @click="openModal(url.id)">Eliminar</span>
              </div>
            </div>
          </div>
          <div class="flex gap-2 mt-3 sm:mt-0">
          </div>
        </li>
      </ul>
      <div class="flex items-center gap-2 justify-center mt-4">
        <button class="border border-zinc-900 p-2 text-xs rounded-xl cursor-pointer text-zinc-70 hover:bg-white hover:text-zinc-950"
          :disabled="currentPage === 1" @click="pagination(currentPage -=1)"> &lt; Previous</button>
        <span class="text-sm">{{ pages.page }} de {{ pages.total_pages }}</span>
        <button class="border border-zinc-900 p-2 text-xs rounded-xl cursor-pointer text-zinc-70 hover:bg-white hover:text-zinc-950"
        @click="pagination(currentPage+=1)" :disabled="urls.total_pages === urls.page">Next &gt;</button>
    </div> 
    </div>
    <div v-else>
        <p class="text-center text-sm">Sem urls criadas</p>
    </div>
    <div v-if="openConfirmation">
          <ConfirmationModal @confirmation="handlerConfirmation" @cancel="openConfirmation = false"/>
      </div>
  </section>
</template>

<script setup>
  import { ref } from 'vue'
  import { copyToClipBoard, createMask, calcConversionRate} from '../utils/extensions'
  import ConfirmationModal from './ConfirmationModal.vue'
  
  const currentPage = ref(1)
  const emits = defineEmits(['page'])
  const openConfirmation = ref(false)
  const urlIDtoDelete = ref(0)
  const apiUrl = ref(import.meta.env.VITE_API_URL)

  const props = defineProps({
      urls : {
        type: Array
      },
      pages: {
        type: Object,
        
      }

    })

    const pagination = function(page){
      currentPage.value = page
      emits('page', currentPage.value)

    }

    const handlerConfirmation = async function(){

      try {
          const request = await fetch(`http://127.0.0.1:8000/delete_url?id=${urlIDtoDelete.value}`, {
            method : 'DELETE'
          })
          
          if(!request.ok){
            console.log("Não foi possível emilinar ma url tente novamente")
            return
          }
          const data = await request.json()

          if(!data.status_code){
            console.log("Houve um erro ao tentar remover a url")
            return
          }
          emits('page', currentPage.value)
          


      }catch(error){

      }
      
    }

    const openModal = function(id){
      urlIDtoDelete.value = id
      openConfirmation.value = !ConfirmationModal.value
    }
</script>
