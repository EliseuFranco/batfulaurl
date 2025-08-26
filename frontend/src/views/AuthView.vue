<template>
    <section>
        <LoginForm v-if="route.name === 'login'"/>
        <RegisterForm v-if=" route.name === 'register'"></RegisterForm>
    </section>
</template>


<script setup>
    import LoginForm from '../components/LoginForm.vue';
    import RegisterForm from '../components/RegisterForm.vue';

    import { onMounted, watch } from 'vue';
    import { useRoute } from 'vue-router';

    const route = useRoute()



</script>