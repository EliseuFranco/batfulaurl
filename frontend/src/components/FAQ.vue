<template>
  <section class="text-zinc-200 p-10">
    <div class="w-full max-w-4xl mx-auto grid gap-5">
      <h3 class="text-xl font-semibold">FAQ'S</h3>
      <div
        v-for="(faq, index) in faqs"
        :key="index"
        class="border-l-4 border-gray-500 p-5 rounded-2xl bg-zinc-900"
      >
        <div class="flex items-center justify-between cursor-pointer" @click="toggleQuestion(index)">
          <h3 class="text-lg font-semibold">{{ faq.pergunta }}</h3>
          <span class="text-2xl font-bold text-purple-500">{{ openQuestion === index ? '-' : '+' }}</span>
        </div>

        <div v-if="openQuestion === index" class="mt-3 text-zinc-300 fade-in">
        <p>{{ faq.resposta }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const openQuestion = ref(null)

const faqs = ref([
  {
    pergunta: 'Como funciona o encurtador de URLs?',
    resposta:
      'Ao inserir um link longo, geramos uma versão curta e única que redireciona para o original. É útil para compartilhamento e rastreamento.'
  },
  {
    pergunta: 'É possível ver quantos cliques uma URL recebeu?',
    resposta:
      'Sim, cada link encurtado registra o número total de cliques, que pode ser consultado nas métricas.'
  },
  {
    pergunta: 'As URLs expiram?',
    resposta:
      'Atualmente, não há expiração automática. Mas futuramente, pretendemos adicionar essa funcionalidade.'
  }
])

function toggleQuestion(index) {
  openQuestion.value = openQuestion.value === index ? null : index
}
</script>


<style scoped>

    @keyframes fade {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    .fade-in {
        animation: fade .5s ease-in-out;
    }

</style>