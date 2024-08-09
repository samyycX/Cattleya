<template>
  <div id="popup-container">
    <div ref="popup" class="top-full flex flex-col gap-5 bg-theme-0 border-2 border-theme-5 min-w-max overflow-visible p-2 text-theme-5 rounded-md">
      <p class="text-2xl min-w-64 text-left">{{ props.params.title }}</p>
      <div class="flex flex-row justify-end gap-2 w-full text-xl">
        <p class="text-theme-5/75 hover:underline underline-offset-4 cursor-pointer" @click="props.params.cancel">取消</p>
        <p class="confirm hover:underline underline-offset-4 cursor-pointer" :style="`color: ${getConfirmColor()}`" @click="() => { props.params.cancel();props.params.confirm();}">确认</p>
      </div>
    </div>
  </div>  
</template>

<script setup>
import { defineProps, ref } from 'vue';
const props = defineProps([ "params" ])
const popup = ref()

const getConfirmColor = () => {
  switch (props.params.type) {
    case "dangerous":
      return "var(--red-800)"
    default:
      return "rgb(var(--theme-5))"
  }
}


</script>