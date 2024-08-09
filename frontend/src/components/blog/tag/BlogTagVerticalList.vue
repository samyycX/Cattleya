<template>
  <div>
    <div class="flex flex-row gap-2 mb-2">
      <TagIcon class="size-7 text-theme-5 my-auto" />
      <p class="text-2xl text-theme-5 text-left">标签</p>
    </div>
    <div v-for="tag in props.tags.toSorted((a, b) => b.blogCount - a.blogCount)" :key="tag.id" class="pr-2 lg:pr-20">
      <div class="flex flex-row w-full justify-between text-theme-5 border-b-[1.5px] border-theme-5 lg:border-transparent hover:border-theme-5 leading-1 border-theme-5 cursor-pointer text-xs lg:text-md">
        <p>{{ tag.name }}</p>
        <p>{{ tag.blogCount }} 篇博客</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { TagIcon } from '@heroicons/vue/24/outline'
import axios from 'axios';
import { defineProps, onMounted } from 'vue';
const props = defineProps(["tags"])

onMounted(async () => {
  for (var tag of props.tags) {
    tag.blogCount = (await axios.get(`/api/blog-tags/${tag.id}/count/`)).data.data;
  }
})

</script>
