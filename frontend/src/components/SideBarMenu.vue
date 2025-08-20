<template>
  <nav class="bg-zinc-900 text-white fixed top-0 p-3 z-50 h-dvh md:p-10 md:z-0 md:sticky md:w-64 transform
    transition-all ease-in-out duration-500" :class="{ 'overflow-x-hidden -ml-64 w-0 p-0': !isOpen }">

    <div class="w-64 flex flex-col gap-4">
      <div class="flex items-center justify-between w-full p-2">
        <p class="font-semibold text-xl">Company logo</p>
        <span
          class="cursor-pointer font-bold text-purple-500 md:hidden"
          @click="closeSideBar">X</span>
      </div>

      <div class="p-2 text-sm">
        <u class="list-none no-underline flex flex-col gap-2">
            <li class="flex items-center gap-2 font-semibold cursor-pointer hover:text-purple-400" @click="openModal">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="lucide lucide-plus-icon lucide-plus text-purple-500">
                <path d="M5 12h14"/><path d="M12 5v14"/></svg>Encurtar url</li>
            <li class="flex items-center gap-3 font-semibold cursor-pointer hover:text-purple-400" @click="scrollToMyUrls">
               <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="lucide lucide-link2-icon lucide-link-2 text-purple-500">
                <path d="M9 17H7A5 5 0 0 1 7 7h2"/><path d="M15 7h2a5 5 0 1 1 0 10h-2"/><line x1="8" x2="16" y1="12" y2="12"/></svg>Minhas urls</li>

            <li class="flex items-center gap-3 font-semibold cursor-pointer hover:text-purple-400"> <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="lucide lucide-cog-icon lucide-cog text-purple-500"><path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/><path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M12 2v2"/><path d="M12 22v-2"/><path d="m17 20.66-1-1.73"/><path d="M11 10.27 7 3.34"/><path d="m20.66 17-1.73-1"/>
                <path d="m3.34 7 1.73 1"/><path d="M14 12h8"/><path d="M2 12h2"/><path d="m20.66 7-1.73 1"/><path d="m3.34 17 1.73-1"/><path d="m17 3.34-1 1.73"/><path d="m11 13.73-4 6.93"/></svg>Configurações</li>
            
                <li class="flex items-center gap-3 font-semibold cursor-pointer hover:text-purple-400"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                     class="lucide lucide-log-out-icon lucide-log-out text-purple-500">
                    <path d="m16 17 5-5-5-5"/><path d="M21 12H9"/><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/></svg>Sair</li>
        </u>
      </div>
    </div>
  </nav>
</template>

<script setup>

    import { eventBus } from '../utils/extensions'

    const props = defineProps({
      isOpen: Boolean
    })

    const emit = defineEmits(['close','open'])

    const closeSideBar = () => {
      emit('close')
    }

    const openModal = function(){
      eventBus.emit('open')
    }

    const scrollToMyUrls = function(){
      eventBus.emit('ScrollToUrls')
    }
</script>
