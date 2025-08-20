<template>
  <section class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md">
      <!-- Título -->
      <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">
        {{ isLogin ? 'Entrar' : 'Criar Conta' }}
      </h2>

      <!-- Formulário -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Apenas no registo -->
        <div v-if="!isLogin">
          <label class="block text-sm font-medium text-gray-700">Nome</label>
          <input
            v-model="form.name"
            type="text"
            class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring focus:ring-purple-300"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring focus:ring-purple-300"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Password</label>
          <input
            v-model="form.password"
            type="password"
            class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring focus:ring-purple-300"
            required
          />
        </div>

        <!-- Botão -->
        <button
          type="submit"
          class="w-full bg-purple-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-purple-700 transition"
        >
          {{ isLogin ? 'Entrar' : 'Registar' }}
        </button>
      </form>

      <!-- Alternar -->
      <p class="mt-4 text-sm text-gray-600 text-center">
        {{ isLogin ? 'Ainda não tens conta?' : 'Já tens conta?' }}
        <button @click="isLogin = !isLogin" class="text-purple-600 font-semibold hover:underline">
          {{ isLogin ? 'Registar' : 'Entrar' }}
        </button>
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const isLogin = ref(true)

const form = ref({
  name: '',
  email: '',
  password: ''
})

const emit = defineEmits(['login', 'register'])

const handleSubmit = () => {
  if (isLogin.value) {
    emit('login', { email: form.value.email, password: form.value.password })
  } else {
    emit('register', form.value)
  }
}
</script>
