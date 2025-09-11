<template>
    <section class="text-white p-3 md: h-full">
        <div class="border border-zinc-900  rounded-2xl transition-all ease-in-out
            duration-500 transform hover:scale-105 shadow hover:shadow-purple-200 shadow-sm h-full flex justify-center">
            <apexchart type="donut" width="380" :options="chartOptions" :series="series"></apexchart>
      </div>
    </section>
</template>


<script setup>

    import { computed, ref} from 'vue';

    const props = defineProps({
        data:{
            type: Array,
            required : true   
        }

    })

    const series = computed(() => props.data.map(valor => Object.values(valor)).flat())
    const labels = computed(() => props.data.map(keys => Object.keys(keys)).flat()).value

    const chartOptions = ref({
        chart: {
            type : 'donut'
        },
        legend: {
            position:'bottom'
        },
        labels: labels,
        colors: ['#6b26d9', '#6666ff', '#b447eb']
    })




</script>