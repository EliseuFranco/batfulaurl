<template>
    <section class="p-5 md:p-10 text-black" >
        <div class="border border-zinc-900  rounded-2xl transition-all ease-in-out duration-500 transform hover:scale-105 shadow hover:shadow-purple-200 shadow-sm">
            <apexchart type="area" height="350" :options="chartOptions" :series="series"></apexchart>
      </div>
    </section>
</template>


<script setup>

import { ref } from 'vue';


    const series = ref([
        {
            name: 'Series 1',
            data: [31, 40, 28, 51, 42, 109, 100]
        },
        {
            name: 'Series 2',
            data: [11, 32, 45, 32, 34, 52, 41]
        }
        ])

    const chartOptions = ref({
            chart: {
                type: 'area',
                toolbar: {
                    show: false
                }
            },
            grid: {
                yaxis: {
                    lines: {
                        show: false
                    }
                }
            }
        })

</script>