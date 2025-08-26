
<template>
  <p class="text-white text-center">A terminar sessão...</p>
</template>




<script setup>

    import { onMounted} from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()

    onMounted(async () => {
    localStorage.removeItem('token')

    setTimeout(()=> {
        console.log('Redirecionando...')
        router.replace('/login?out=true')
    }, 1000)

    console.log("Logout route")
    })
</script>

