<template>
    <section class="p-8 rounded-xl shadow-sm/50 border border-zinc-900 shadow-purple-600">
        <div>
            <p class="text-right mb-5 cursor-pointer text-2xl font-semibold" @click="closeModal" v-if="hideButton">X</p>
            <h2 class="font-bold">Encurtar novo link</h2>
            <p class="text-zinc-500">Cole sua URL longa abaixo e receba um link curto instantaneamente</p>
        </div>
        <form class="mt-4 w-full flex gap-2 items-center" @submit.prevent="get_url">
            <input type="text" name="" id="" placeholder="http://exemplo.com/link-gigante" v-model="url" required
             class="w-full p-2 border text-zinc-400 border-zinc-900 rounded-2xl outline-none focus:border-purple-800 focus:border-2">
            <button class="bg-gradient-to-r from-purple-600 to-fuchsia-800 p-3 rounded-xl animate-pulse shadow-purple-600 cursor-pointer">Encurtar</button>
        </form>
    </section>
</template>

<script setup>

    import { ref } from 'vue'
    import { eventBus } from '../utils/extensions'

    const url = ref('')
    const emits = defineEmits(['regist', 'update','open','close'])
    const props = defineProps(['hideButton'])


    const get_url = function () {

        emits('regist', {url: url.value})
        emits('update')
        emits('close')
        url.value = ''
    }

    const closeModal = function(){
        eventBus.emit('close')
    }


</script>