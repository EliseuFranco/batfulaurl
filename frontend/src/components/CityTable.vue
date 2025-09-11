<template>
  <section class="p-3 md:p-10 text-white">
    <table class="w-full h-full border border-white bg-zinc-900 rounded-xl overflow-hidden text-sm text-zinc-200">
      <thead class="bg-zinc-800 text-left">
        <tr>
          <th class="p-3">Cidade</th>
          <th class="p-3">Hora</th>
          <th class="p-3">Clicks Únicos</th>
          <th class="p-3">Total de Clicks</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index" class="border-t border-zinc-800 hover:bg-zinc-950">
          <td class="p-3">{{ row.city || 'Luanda' }}</td>
          <td class="p-3">{{ row.hour }}</td>
          <td class="p-3">{{ row.unique_clicks }}</td>
          <td class="p-3">{{ row.total_clicks }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
import { ref } from "vue"



const props = defineProps({
    data: {
      type: Array
    }
})
const rows = ref([
  { cidade: "Lisboa", hora: "10:30", clicks_unicos: 12, total_clicks: 18 },
  { cidade: "Porto", hora: "11:15", clicks_unicos: 5, total_clicks: 7 },
  { cidade: "Luanda", hora: "12:00", clicks_unicos: 20, total_clicks: 25 }
])
</script>
