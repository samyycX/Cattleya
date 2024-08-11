<template>
    <div class="flex flex-col text-left border-l-4 px-2 w-full" :style="`border-color: ${statusColor}`">
        <p :style="`color: ${statusColor}`" class="text-sm md:text-lg">{{ props.task.title }}</p>
        <div class="flex flex-row">
            <p :style="`color: ${statusColor}`" class="leading-none text-sm text-nowrap w-2/12 text-center">{{ status }}</p>
            <div class="flex flex-row w-full leading-none opacity-50 overflow-x-hidden text-nowrap" v-if="props.task.progress != 'fail'">
                <p :style="`color: ${statusColor}`" class=" text-xs md:text-md">{{ props.task.progress == 'success' ? "#".repeat(CHAR_NUM) : "#".repeat(parseInt(props.task.progress/100*CHAR_NUM)) }}</p>
                <p class="text-theme-5 text-xs md:text-md">{{ "-".repeat(CHAR_NUM - parseInt(props.task.progress/100*CHAR_NUM)) }}</p>
            </div>
            <div class="" v-else>
                <p class="leading-none text-red-700 text-xs">{{  props.task.msg }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, defineProps, ref } from 'vue';

const CHAR_NUM = 40

const props = defineProps(["task"])


const status = computed(() => {
    if (props.task.progress == "success") {
        return "成功"
    }
    if (props.task.progress == "fail") {
        return "失败"
    }
    return `${parseInt(props.task.progress)}%`
})

const statusColor = computed(() => {
    if (props.task.progress == "success") {
        return "rgb(var(--theme-4))"
    }
    if (props.task.progress == "fail") {
        return "var(--red-800)"
    }
    return "rgb(var(--theme-5))"
})

</script>

