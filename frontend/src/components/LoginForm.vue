<template>
    <section class="flex flex-col">
        <div>
            <Message :msg="msg"/>
        </div>
        <div class="h-screen flex flex-col items-center justify-center text-white">
            <h3 class="text-center mb-5 text-xl font-semibold">Seja bem-vindo(a) de volta</h3>
            <div class="grid md:grid-cols-2 w-full max-w-4xl p-5 text-sm">
                <form class="w-full bg-zinc-900 rounded-tl-xl rounded-tr-xl p-10 space-y-5 md:rounded-l-xl md:rounded-tr-none" @submit.prevent="login">
                    <div class="flex flex-col gap-2">
                        <label for="email" class="font-semibold">Email</label>
                        <input type="email" name="email" id="email" placeholder="Email" class="border border-zinc-700 p-2 rounded-xl" v-model="email" required>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="password" class="font-semibold">Password</label>
                        <input type="password" name="password" id="password" placeholder="Password" class="border border-zinc-700 p-2 rounded-xl" v-model="password" required>
                    </div>
                    <button class="bg-purple-800 w-full mt-5 p-2 rounded-xl cursor-pointer hover:bg-purple-900">Iniciar sessão</button>
                </form>
                <div class="bg-gradient-to-r from-purple-950 to-purple-600 w-full p-10 md:rounded-r-xl flex flex-col rounded-bl-xl rounded-br-xl md:
                 md:rounded-bl-none text-sm">
                    <p>Não tem uma conta ? <router-link to="/register" class="font-semibold underline">Criar conta</router-link></p>
                    <p>E começa a impulsionar as tuas campnhas de marketing</p>
                    <ul class="list-none mt-2">
                        <li class="before:content-['✓']"> Encurtar urls</li>
                        <li class="before:content-['✓']"> Estatisticas</li>
                        <li class="before:content-['✓']"> URL fácil de partilhar</li>
                
                    </ul>
                </div>
            </div>
        </div>

    </section>
</template>


<script setup>

    import { ref, onMounted } from 'vue';
    import Message from './Message.vue'
    import { eventBus } from '../utils/extensions';
    import { useRoute, useRouter } from 'vue-router';

    const email = ref('')
    const password = ref('')
    const msg = ref('')
    const route = useRoute()
    const router = useRouter()

    const login = async function() {

        const user_to_login = {email: email.value, password_hash: password.value}
        const apiUrl = import.meta.env.VITE_API_URL

        const request = await fetch(`${apiUrl}/login`, {

            method: 'POST',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify(user_to_login)
        })

        const data = await request.json()

        if (!data.token){
            msg.value = data.msg;
            return
        }
        localStorage.setItem('token', data.token)
        router.push("/dashboard")


    }

    onMounted(()=>{
        if(route.query.out){
            msg.value = 'Sessão terminada...'
        } else if(route.query.sessionExpired){
            msg.value = 'Sua sessão expirou, faça login novamente'
        }
        
    })


</script>