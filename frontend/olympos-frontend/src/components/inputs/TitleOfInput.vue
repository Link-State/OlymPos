<template>
    <div class="input_title">
        <slot></slot>
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.input_title {
    padding: 10px 0;
    font-weight: bold;
    font-size: 13px;
    border-bottom: 1px solid var(--main-gray-3);
}
</style>