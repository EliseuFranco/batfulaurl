<template>
    <section class="p-3 md:p-10 text-black w-full ">
        <div class="border border-zinc-900  rounded-2xl transition-all ease-in-out duration-500 transform hover:scale-105 shadow hover:shadow-purple-200 shadow-sm">
        <apexchart height="350" width="95%" :options="chartOptions" :series="series"></apexchart>
      </div>
    </section>
</template>


<script setup>
    import { ref, computed } from 'vue';

    const series = computed(() => [{
            data: [400, 430, 448, 470]
          }])

    const chartOptions = ref({
        chart: {
            type: 'bar',
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
        plotOptions: {
            bar: {
                horizontal: true
            }
        },
        dataLabels: {
            enabled: false
          },
        xaxis : {
            categories: ['Angola', 'Cabo verde','Camarões', 'Guiné bissau']
        },
    })

</script>