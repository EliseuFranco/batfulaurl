<template>
     <section>
        <div class="bg-green-200">
            <Message :msg="msg"/>
        </div>
        <div class="grid md:grid-cols-3 gap-3 p-7 w-full f-full max-w-5xl text-sm text-zinc-300">
            <div class="border border-purple-500 rounded-2xl p-7" v-for="(url, index) in all_url" :key="index">
                <div class="flex justify-end mb-3">
                    <button class="text-right cursor-pointer" @click="copyToClipBoard(url.shortened_url)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-copy-icon lucide-copy">
                            <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                    </button>
                </div>
                <p class="flex items-center gap-2 mb-3">{{ url.shortened_url }}
                    <a :href="'http://127.0.0.1:8000/redirect?user_slug=' + getSlug(url.shortened_url)" target="_blank">
                        
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                         class="lucide lucide-external-link-icon lucide-external-link text-purple-300">
                            <path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
                    </a>
                </p>
                <a :href="url.original_url" target="_blank" class="hover:text-zinc-500"><span class="text-purple-400">Link original</span>: {{ createMask(url.original_url) }}</a>
            </div>
        </div>
     </section>

</template>

<script setup>

    import { ref } from 'vue'
    import Message from './Message.vue'

    const props = defineProps(['all_url'])
    const emit = defineEmits(['msg'])
    const msg = ref('')

    const createMask = (url) => {
        try {
            const parsed = new URL(url)
            const domain = parsed.hostname
            return domain.length > 25 ? domain.slice(0, 25) + '...' : domain
        } catch (error) {
            return url.length > 30 ? url.slice(0, 30) + '...' : url
        }
    }

    const copyToClipBoard = async function(text) {
        
        try{
            navigator.clipboard.writeText(text)
            emit('msg', 'URL copiada para área de transferência')
        }
        catch(error){
            console.log("Algo correu mal")
        }

    }

    const getSlug = function(shorten_url){
        if(!shorten_url){
            return ''
        }
        const ArrayURL = shorten_url.split('/')
        const size = ArrayURL.length
        return ArrayURL[size - 1]
    }

</script>