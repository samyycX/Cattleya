<template>
  <div class="bg-theme-4 flex flex-row px-2">
    <p class="text-theme-0">{{ name }}</p>
    <div class="flex flex-col justify-center" @click="cancel">
      <XMarkIcon class="size-4 text-theme-0 cursor-pointer hover:text-theme-2" v-if="props.cancelable" />
    </div>
  </div>
</template>

<script setup>
import { XMarkIcon } from '@heroicons/vue/24/solid';
import { defineProps, defineEmits } from 'vue';

const emit = defineEmits(["cancel"])
const props = defineProps(["name", "cancelable"])

const cancel = () => emit('cancel')

</script>
