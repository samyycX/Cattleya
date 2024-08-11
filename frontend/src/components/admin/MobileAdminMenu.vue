<template>
  <div>
    <div class="flex flex-col gap-3 border-b-2 border-theme-5 pb-3 py-3 text-theme-5">
      <div class="flex flex-row justify-between">
        <p class="text-xl">管理</p>
        <Bars3Icon class="size-6" v-if="!expanded" @click="expanded = true"/>
        <XMarkIcon class="size-6" v-else @click="expanded = false"/>
      </div>
      <AdminMenu class="text-left" v-if="expanded" v-model="mode" />
    </div>
  </div>
</template>

<script setup>
import AdminMenu from './AdminMenu.vue';
import { Bars3Icon } from '@heroicons/vue/24/outline';
import { XMarkIcon } from '@heroicons/vue/24/solid';
import { ref } from 'vue';
import { defineModel } from 'vue';
const mode = defineModel()


const expanded = ref(false)

</script>
