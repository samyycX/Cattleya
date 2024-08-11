<template>
  <div class="absolute w-screen h-screen left-0 top-0 flex flex-col justify-center backdrop-blur" v-if="tasks.length != 0">
    <div class="flex flex-col gap-3 mx-auto bg-theme-0 border-theme-5 border-2 h-4/6 w-11/12 md:w-4/6 lg:w-1/3 px-10 py-5 rounded-lg">
      <p class="text-2xl text-theme-6 text-left">{{ `共 ${tasks.length} 项，已完成 ${tasks.filter(task => task.progress == 'success').length} 项，失败 ${tasks.filter(task => task.progress == 'fail').length} 项` }}</p>
      <div class="flex flex-col gap-3 h-4/6 overflow-y-scroll ">
        <div v-for="(task, index) in tasks" :key="index">
          <ProgressBar :task="task" />
        </div>
      </div>
      <div class="flex flex-row mt-auto mb-2 w-full justify-end">
        <button class="bg-theme-5 text-theme-0 p-2 rounded-md leading-none disabled:bg-theme-5/50" :disabled="!isAllCompleted" @click="onAllDone">确认</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProgress } from '@/stores/progresses';
import { storeToRefs } from 'pinia';
import ProgressBar from './general/ProgressBar.vue';
import { computed } from 'vue';


const progressStore = useProgress();
const { onAllDone, tasks } = storeToRefs(progressStore);

const isComplete = (task) => {
  return task.progress == 'success' || task.progress == 'fail'
}

const isAllCompleted = computed(() => !tasks.value.map(isComplete).includes(false))

</script>
<style scoped>
::-webkit-scrollbar {
    display: none;
}
</style>