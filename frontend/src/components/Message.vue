<template>

    <section v-if="msg" class="fixed w-full flex top-0 p-2 justify-center">
        <div class="bg-purple-500 p-2 rounded ">
            <p class="text-white">{{ msg }}</p>
        </div>
    </section>


</template>

<script setup>


const props = defineProps(['msg'])

</script>