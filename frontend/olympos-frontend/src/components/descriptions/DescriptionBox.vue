<template>
    <div class="description" :class="props.state">
        <slot></slot>
    </div>
</template>

<script setup lang="ts">

const props = defineProps(["state"]);



</script>

<style scoped>
.description {
    padding: 10px;
    height: 32px;
    background-color: var(--main-gray-3);
    font-size: 10px;
    color: var(--main-black-soft);
    line-height: 12px;
}
.info {
    background-color: var(--main-mute-1);
    color: var(--main-black-soft);
}
.warn {
    /* Todo */
}
</style>