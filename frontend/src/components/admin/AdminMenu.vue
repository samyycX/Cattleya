<template>
  <div>
    <div class="flex flex-col gap-2 text-theme-5">
      <p class="cursor-pointer hover:underline underline-offset-4" @click="() => to('blog')">博客</p>
      <p class="cursor-pointer hover:underline underline-offset-4" @click="() => to('blog-tag')">博客标签</p>
      <p class="cursor-pointer hover:underline underline-offset-4" @click="() => to('file')">文件</p>
      <p class="cursor-pointer hover:underline underline-offset-4 md:mt-5" @click="toMainpage">返回主页</p>
    </div>
  </div>
</template>

<script setup>
import { defineModel } from 'vue';
import { useRouter } from 'vue-router';
const mode = defineModel()
const router = useRouter()

const to = (newMode) => {
  mode.value = newMode;
}
const toMainpage = () => {
  router.push({ name: 'mainpage' })
}
</script>