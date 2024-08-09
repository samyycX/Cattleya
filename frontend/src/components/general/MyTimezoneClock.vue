<template>
  <div>
    <div class="flex flex-row gap-2 text-left">
        <ClockIcon class="size-6 text-theme-5" v-if="!isMobile" />
        <p class="text-theme-5">{{ myTime }} (UTC+8)</p>
    </div>
  </div>
</template>

<script setup>
import { isMobile } from '@/utils';
import { ClockIcon } from '@heroicons/vue/24/outline';
import { ref, onMounted, onUnmounted } from 'vue';
const myTime = ref("..")
var clockTimerId;
onMounted(() => {
  clockTimerId = setInterval( function getMyTime() {
    myTime.value = new Date().toLocaleString("zh-CN", { hour: '2-digit', hour12: false, minute: '2-digit', second: '2-digit' }).split(" ").at(-1)
    return getMyTime
   }(), 1000)
})

onUnmounted(() => {
  clearInterval(clockTimerId);
})
</script>
