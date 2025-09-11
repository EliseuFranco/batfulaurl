<template>
    <section class="p-3 text-black w-full">
        <div class="border border-zinc-900  rounded-2xl transition-all ease-in-out duration-500 transform hover:scale-100
         shadow hover:shadow-purple-200 shadow-sm
        mx-auto">
            <apexchart type="area" height="350" width="100%" :options="chartOptions" :series="series"></apexchart>
      </div>

    </section>
</template>


<script setup>

    import { ref, computed } from 'vue';

    const props = defineProps({

        chartData: {
            type: Array,
            required: true
        },
        chartData2: {
            type: Array,
            required: true
        }
    })

    const series = computed(() => [
        {
            name: 'Total clicks',
            data: props.chartData.map(({data,clicks}) =>{
                return {
                    x: new Date(data).getTime(),
                    y : clicks
                }
            })
        },
        {
            name: 'Clicks únicos',
            data: props.chartData2.map(({data, clicks}) => {
                return {
                    x: new Date(data).getTime(),
                    y: clicks
                }
            })
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
            },
            xaxis: {
                type: 'datetime'
            },
        })

</script>