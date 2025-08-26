<template>
    <section class="bg-black/75 fixed top-0 left-0 w-full h-dvh flex items-center justify-center">
        <div class="bg-purple-800 w-ful max-w-3xl p-10 flex flex-col gap-7">
            <p>Certeza que querer eliminar a url "{{ url_id }}" ?</p>
            <div class=" flex items-center gap-3">
                <button class="grow border border-zinc-900 bg-black rounded p-1 cursor-pointer" @click="btnConfirm">Confirmar</button>
                <button class="border p-1 rounded border-zinc-900 cursor-pointer" @click="btnCancel">Cancelar</button>
            </div>
        </div>
    </section>
</template>

<script setup>

    const props = defineProps({
        url : String,
        url_id : Number
    })
    const emits = defineEmits(['confirmation','cancel', 'close'])

    const btnConfirm = function(){
        emits('confirmation')
        emits('close')
    }

    const btnCancel = function(){
        emits('cancel')
    }

</script>
