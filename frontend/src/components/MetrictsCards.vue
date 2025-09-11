<template>
    <section>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 xl:grid-cols-4 gap-5 -mt-5">
            <div class="border border-zinc-900 bg-blue-200 p-3 md:p-5 rounded-2xl transition-all ease-in-out duration-500 transform hover:scale-105 shadow hover:shadow-purple-200 shadow-sm">
                <div class="flex items-center justify-between space-y-4">
                    <h1 class="text-zinc-400 text-sm">Total de clicks</h1>
                    <span class="bg-gradient-to-r from-purple-500 to-purple-800 p-1 rounded">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                         class="lucide lucide-mouse-pointer-click-icon lucide-mouse-pointer-click"><path d="M14 4.1 12 6"/><path d="m5.1 8-2.9-.8"/><path d="m6 12-1.9 2"/><path d="M7.2 2.2 8 5.1"/>
                            <path d="M9.037 9.69a.498.498 0 0 1 .653-.653l11 4.5a.5.5 0 0 1-.074.949l-4.349 1.041a1 1 0 0 0-.74.739l-1.04 4.35a.5.5 0 0 1-.95.074z"/></svg>
                    </span>
                </div>
                <h1 class="font-bold text-2xl">{{ data.total_clicks || 0  }}</h1>
                <p class="text-xs text-zinc-400"><span class="text-green-400">15.4</span> % vs o mês anterior</p>
            </div>
            <div class="border border-zinc-900 p-5 rounded-2xl transition-all ease-in-out duration-500 transform hover:scale-105 shadow hover:shadow-purple-200 shadow-sm">
                <div class="flex items-center justify-between space-y-4">
                    <h1 class="text-zinc-400 text-sm">Clicks Únicos</h1>
                    <span class="bg-gradient-to-r from-purple-500 to-purple-800 p-1 rounded">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                         class="lucide lucide-users-round-icon lucide-users-round">
                            <path d="M18 21a8 8 0 0 0-16 0"/><circle cx="10" cy="8" r="5"/>
                            <path d="M22 20c0-3.37-2-6.5-4-8a5 5 0 0 0-.45-8.3"/></svg>
                    </span>
                </div>
                <h1 class="font-bold text-2xl">{{ data.unique_clicks || 0 }}</h1>
                <p class="text-xs text-zinc-400"><span class="text-green-400">15.4</span> % vs o mês anterior</p>
            </div>
            <div class="border border-zinc-900 p-5 rounded-2xl transition-all ease-in-out duration-500 transform hover:scale-105 shadow hover:shadow-purple-200 shadow-sm">
                <div class="flex items-center justify-between space-y-4">
                    <h1 class="text-zinc-400 text-sm">Taxa de conversão</h1>
                    <span class="bg-gradient-to-r from-purple-500 to-purple-800 p-1 rounded">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-trending-up-icon lucide-trending-up">
                            <path d="M16 7h6v6"/><path d="m22 7-8.5 8.5-5-5L2 17"/></svg>
                    </span>
                </div>
                <h1 class="font-bold text-2xl">{{ calcConversionRate(data.unique_clicks, data.total_clicks) }}%</h1>
                <p class="text-xs text-zinc-400"><span class="text-green-400">15.4</span> % vs o mês anterior</p>
            </div>
            <div class="border border-zinc-900 p-5 rounded-2xl transition-all ease-in-out duration-500 transform hover:scale-105 shadow hover:shadow-purple-200 shadow-sm">
                <div class="flex items-center justify-between space-y-4">
                    <h1 class="text-zinc-400 text-sm">Total de países </h1>
                    <span class="bg-gradient-to-r from-purple-500 to-purple-800 p-1 rounded">
                       <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-globe-icon lucide-globe"><circle cx="12" cy="12" r="10"/>
                        <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
                    </span>
                </div>
                <h1 class="font-bold text-2xl">{{ data.total_by_country || 0 }}</h1>
                <p class="text-xs text-zinc-400"><span class="text-green-400">15.4</span> % vs o mês anterior</p>
            </div>
            
           
        </div>
    </section>
</template>


<script setup>

    import { eventBus, calcConversionRate } from '../utils/extensions';

    const props = defineProps({
        data: {
            type: Object
        } 
        })
</script>