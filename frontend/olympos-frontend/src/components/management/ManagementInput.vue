<template>
    <div>
        <TitleOfInput>{{ props.title }}</TitleOfInput>
        <inputWithoutBorder :type="props.type" :placeholder="props.placeholder" :value="props.modelValue" @changeInput="changeInput"></inputWithoutBorder>
    </div>
</template>

<script setup lang="ts">
import TitleOfInput from '@/components/inputs/TitleOfInput.vue';
import inputWithoutBorder from '@/components/inputs/inputWithoutBorder.vue';

const props = defineProps({
    type: String,
    title: String,
    placeholder: String,
    modelValue: [String, Number],
});
const emit = defineEmits(['update:modelValue']);
const changeInput = (changedValue: string)=>{
    emit('update:modelValue', changedValue);
}
</script>

<style scoped>
</style>