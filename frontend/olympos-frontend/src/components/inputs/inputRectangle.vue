<template>
    <input :type="props.type" :placeholder="dynamicPlaceholder" @focus="focus" @blur="blur" @input="changeInput" :value="props.modelValue">
</template>

<script setup lang="ts">
import { ref } from 'vue';


const props = defineProps({
    type: String,
    title: String,
    placeholder: String,
    modelValue: [String, Number],
});

const emit = defineEmits(['changeInput']);
const changeInput = (event: Event)=>{
    if(event.target !== null){
        emit('changeInput', (event.target as HTMLInputElement).value);
    }
}


const dynamicPlaceholder = ref(props.placeholder);
const focus = ()=>{
    dynamicPlaceholder.value = '';
}
const blur = ()=>{
    dynamicPlaceholder.value = props.placeholder;
}
</script>

<style scoped>
input {
    padding: 16px;
    width: -webkit-fill-available;
    border: 1px solid var(--main-gray-3);
    border-radius: 5px;
}
input:focus {
    border: 1px solid var(--main);
    outline: 1px solid var(--main);
}
input::placeholder {
    color: var(--main-gray-1);
}
</style>