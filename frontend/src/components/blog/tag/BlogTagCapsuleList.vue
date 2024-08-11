<template>
  <div>
    <div class="flex flex-row gap-2 mb-2">
      <TagIcon class="size-7 text-theme-5 my-auto" />
      <p class="text-2xl text-theme-5 text-left">标签</p>
    </div>
    <div class="flex flex-row flex-wrap gap-2" v-if="props.tags">
      <div v-for="tag in props.tags.toSorted((a, b) => b.count - a.count)" :key="tag.id">
        <div class="flex flex-row gap-2 text-theme-0 bg-theme-5 p-1 cursor-pointer text-sm leading-none rounded-md" @click="() => toBlogTag(tag)">
          <p>{{ tag.name }}</p>
          <p class="bg-theme-0 rounded-[4px] text-theme-5 px-1">{{ tag.count }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { TagIcon } from '@heroicons/vue/24/outline'
import { defineProps } from 'vue';
const props = defineProps(["tags"])
const toBlogTag = (tag) => {
  window.location.href = `/blog/list?tag=${tag.id}`
}
</script>
