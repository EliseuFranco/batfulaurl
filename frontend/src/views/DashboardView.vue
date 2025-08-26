<template>
    <section class="text-white">
        <div class="flex">
            <SideBarMenu :isOpen="isMobile" @close="isMobile = false"/>
            <Dashboard @close="handlerClose"/>
        </div>
    </section>
</template>


<script setup>
    import { ref, onMounted, onBeforeUnmount, watch } from "vue"
    import Dashboard from '../components/Dashboard.vue';
    import SideBarMenu from '../components/SideBarMenu.vue';

    const isMobile = ref(window.innerWidth < 768)

    const handlerClose = function(data){
        
        isMobile.value = !isMobile.value
    }


    function getWindowWidth() {
    if (window.innerWidth < 768) {
        isMobile.value = false
    } else {
        isMobile.value = true
    }
    }

 
    onMounted(() => {
    getWindowWidth()
    window.addEventListener("resize", getWindowWidth)
    })

    onBeforeUnmount(() => {
    window.removeEventListener("resize", getWindowWidth)
    })

</script>