<template>
  <div class="h-full w-full flex flex-row bg-theme-1 text-left">
    <div class="w-1/2 border-theme-5 relative p-2">
      <textarea class="outline-none h-full w-full resize-none bg-theme-1" placeholder="在此处输入..." v-model="content" />
    </div>
    <div class="h-[95%] w-[2px] bg-theme-5 my-auto"></div>
    <div id="preview" class="flex w-1/2 prose prose-cattleya p-2 overflow-y-scroll overflow-x-hidden">
      <BlogMdxRender :content="content" />
    </div>
  </div>
</template>

<script setup>
import BlogEditor from '@/components/blog/BlogEditor.vue';
import BlogMdxRender from '@/components/blog/BlogMdxRender.vue';
import { ref } from 'vue';

const content = ref("");

const input = (val) => {
  content.value = val;
  var elem =document.getElementById("preview");
  elem.scrollTop = elem.scrollHeight;
}
</script>

<style scoped>
div::-webkit-scrollbar {
  background-color: var(--theme-1);
}
div::-webkit-scrollbar-thumb:hover {
  background-color: var(--theme-4);
}
</style>
