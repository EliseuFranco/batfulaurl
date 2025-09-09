<template>
    <section class="h-screen flex flex-col md:flex-row items-center justify-center text-white">
        <Message :msg="msg"/>
        <div class="">
            <h3 class="text-center mb-5 text-xl font-semibold">Criar conta</h3>
            <div class="grid md:grid-cols-2 w-full max-w-4xl p-5 text-sm">
                <form class="w-full bg-zinc-900 rounded-tl-xl rounded-tr-xl p-10 space-y-5 md:rounded-l-xl md:rounded-tr-none" @submit.prevent="register">
                    <div class="flex flex-col gap-2">
                        <label for="nome" class="font-semibold">Nome</label>
                        <input type="nome" name="nome" id="nome" placeholder="Nome" class="border border-zinc-700 p-2 rounded-xl" v-model="nome" required>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="email" class="font-semibold">Email</label>
                        <input type="email" name="email" id="email" placeholder="Email" class="border border-zinc-700 p-2 rounded-xl" v-model="email" required>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="password" class="font-semibold">Palavra-passe</label>
                        <input type="password" name="password" id="password" placeholder="Password" class="border border-zinc-700 p-2 rounded-xl" v-model="password" required>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="password_confirm" class="font-semibold">Confirmar palavra-passe</label>
                        <input type="password" name="password_confirm" id="password_confirm" placeholder="Confirmar palavra-passe" class="border border-zinc-700 p-2 rounded-xl" v-model="passwordConfirmation" required>
                        <span class="text-xs text-red-400">{{ errorMsg }}</span>
                    </div>
                    <button class="bg-purple-800 w-full mt-5 p-2 rounded-xl cursor-pointer hover:bg-purple-900">Criar conta</button>
                </form>
                <div class="bg-gradient-to-r from-purple-950 to-purple-600 w-full p-10 md:rounded-r-xl flex flex-col rounded-bl-xl rounded-br-xl md:
                 md:rounded-bl-none text-sm items-center justify-center">
                    <p>Já tem uma conta? <router-link to="/login" class="font-semibold underline">Iniciar sessão</router-link></p>
                    <p class="text-center mt-2">E visualize as métricas das suas campanhas de marketing</p>
                </div>
            </div>
        </div>

    </section>
</template>


<script setup>
    import { ref } from 'vue';
    import Message from './Message.vue';
    import { useRouter } from 'vue-router';


    const nome = ref('')
    const email = ref('')
    const password = ref('')
    const passwordConfirmation = ref('')
    const errorMsg = ref('')
    const msg = ref('')

    const router = useRouter()


    const register = async function() {

        console.log(router)
        if(password.value !== passwordConfirmation.value ){
            errorMsg.value = 'Palavra-passe não coincidem'
            return
        }
        const userToCreate = {nome: nome.value, email: email.value, password_hash: password.value}
        
        const apiUrl = import.meta.env.VITE_API_URL;
        const request = await fetch(`${apiUrl}/create`, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body : JSON.stringify(userToCreate)
        })
        const data = await request.json()

        if (data.status_code === 409) {
            msg.value = data.msg
            return
        }
        router.push('/dashboard')
    }

</script>