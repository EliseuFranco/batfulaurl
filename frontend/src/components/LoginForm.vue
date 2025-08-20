<template>
    <section class="h-screen flex flex-col md:flex-row items-center justify-center text-white">
     
        <div class="">
            <h3 class="text-center mb-5 text-xl font-semibold">Seja bem-vindo(a) de volta</h3>
            <div class="grid md:grid-cols-2 w-full max-w-4xl p-5 text-sm">
                <form class="w-full bg-zinc-900 rounded-tl-xl rounded-tr-xl p-10 space-y-5 md:rounded-l-xl md:rounded-tr-none" @submit.prevent="login">
                    <div class="flex flex-col gap-2">
                        <label for="email" class="font-semibold">Email</label>
                        <input type="email" name="email" id="email" placeholder="Email" class="border border-zinc-700 p-2 rounded-xl" v-model="email">
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="password" class="font-semibold">Password</label>
                        <input type="password" name="password" id="password" placeholder="Password" class="border border-zinc-700 p-2 rounded-xl" v-model="password">
                    </div>
                    <button class="bg-purple-800 w-full mt-5 p-2 rounded-xl cursor-pointer hover:bg-purple-900">Iniciar sessão</button>
                </form>
                <div class="bg-gradient-to-r from-purple-950 to-purple-600 w-full p-10 md:rounded-r-xl flex flex-col rounded-bl-xl rounded-br-xl md:
                 md:rounded-bl-none text-sm">
                    <p>Não tem uma conta ? <a href="/register" class="font-semibold underline">Criar conta</a></p>
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

    import { ref } from 'vue';

    const email = ref('')
    const password = ref('')

    const login = async function() {

        const user_to_login = {email: email.value, password_hash: password.value}

        const request = await fetch('http://127.0.0.1:8000/login', {

            method: 'POST',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify(user_to_login)
        })

        const data = await request.json()

        console.log(data)
    }

</script>