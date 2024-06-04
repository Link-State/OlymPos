<template>
    <ManagementView>
        <template #title>
            메뉴 그룹 관리
        </template>

        <template #form>
            <TitleOfInput>메뉴 그룹</TitleOfInput>
            <DescriptionBox class="description" :state="'info'">카테고리 이름을 추가할 수 있어요.</DescriptionBox>
            <inputRectangle :type="'text'" :placeholder="'메뉴 그룹 명'" v-model="menuGroup" @changeInput="changeInput"></inputRectangle>
            <!-- todo: 드래그 드랍이 가능한 메뉴 그룹 목록 -->
        </template>

        <template #btnArea>
            <ManagementButton :btnColor="'white'" @click="cancelForm">취소</ManagementButton>
            <ManagementButton :btnColor="'blue'" @click.once="handleSave" :key="buttonKey">저장</ManagementButton>
        </template>
    </ManagementView>
</template>

<script setup lang="ts">
import ManagementView from '@/components/management/ManagementView.vue';
import inputRectangle from '@/components/inputs/inputRectangle.vue';
import ManagementButton from '@/components/management/ManagementButton.vue';
import TitleOfInput from '@/components/inputs/TitleOfInput.vue';
import DescriptionBox from '@/components/descriptions/DescriptionBox.vue';
import { ref } from 'vue';

const menuGroup = ref<string>('');
const changeInput = (changeValue: string)=>{
    menuGroup.value = changeValue;
}



const buttonKey = ref(0);
const increaseButtonKey = () => {
    buttonKey.value++;
}
const cancelForm = ()=>{

}
const handleSave = ()=>{

}
</script>

<style scoped>
.description {
    margin-top: -20px;
}
</style>