<template>
  <section class="w-full text-sm text-zinc-300 flex justify-center p-10 items-center bg-zinc-900">
    <div class="w-full max-w-4xl mx-auto grid md:grid-cols-3 gap-3 p-5">
      
      <div class="border-l-4 border-purple-500 rounded-2xl p-7 flex flex-col items-center gap-3">
        <div class="flex flex-col justify-center items-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
           class="lucide lucide-link-icon lucide-link text-purple-500">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
            <h2 class="text-xl font-semibold text-white">URLs encurtadas</h2>
        </div>
        <p class="text-3xl font-bold mt-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-blue-200">
          {{ metrica.url_shortned || 0 }}
        </p>
      </div>

      <div class="border-l-4 border-purple-500 rounded-2xl p-7 flex flex-col items-center gap-3">
        <div class="flex flex-col justify-center items-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             class="lucide lucide-mouse-icon lucide-mouse text-purple-500"><rect x="5" y="2" width="14" height="20" rx="7"/><path d="M12 6v4"/></svg>
            <h2 class="text-xl font-semibold ">Total de clicks</h2>
        </div>
        <p class="text-3xl font-bold mt-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-blue-200">
          {{ metrica.clicks || 0 }}
        </p>
      </div>
    <div class="border-l-4 border-purple-500 rounded-2xl p-7 flex flex-col items-center gap-3">
        <div class="flex flex-col justify-center items-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             class="lucide lucide-eye-icon lucide-eye text-purple-500">
                <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg>
            <h2 class="text-xl font-semibold text-white">Visitantes únicos</h2>
        </div>  
        <p class="text-3xl font-bold mt-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-blue-200">
          {{ metrica.unique_users }}
        </p>
      </div>
      
    </div>
  </section>
</template>

<script setup>

import { onMounted, ref, watch } from 'vue'

const props = defineProps({
  refresh: Number
})

const emits = defineEmits(['metrics', 'update'])
const metrica = ref({})

const getMetrics = async function () {
  try {
    const request = await fetch('http://127.0.0.1:8000/metrics', { method: 'GET' })

    if (!request.ok) {
      emits('metrics', 'Não foi possível carregar dados')
      return
    }

    const data = await request.json()
    metrica.value = data
    console.log(data)
    emits('update')
  } catch (error) {
    emits('metrics', 'Houve um erro na conexão com o servidor')
    return
  }
}

onMounted(() => getMetrics())

watch(() => props.refresh, () => {
  getMetrics()
})
</script>
