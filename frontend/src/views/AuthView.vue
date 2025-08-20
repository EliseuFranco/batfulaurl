<template>
    <section>
        <LoginForm v-if="$route.fullPath === '/login'"/>
        <RegisterForm v-if="$route.fullPath === '/register'"></RegisterForm>
    </section>
</template>


<script setup>
    import LoginForm from '../components/LoginForm.vue';
    import RegisterForm from '../components/RegisterForm.vue';


</script>