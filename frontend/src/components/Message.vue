<template>

    <section v-if="msg" class="w-full flex justify-center items-center relative bg-blue-200">
        <div class="bg-purple-900 p-2 fixed top-5 rounded">
            <p class="text-white text-sm text-center">{{ msg }}</p>
        </div>
    </section>


</template>

<script setup>


const props = defineProps(['msg'])

</script>