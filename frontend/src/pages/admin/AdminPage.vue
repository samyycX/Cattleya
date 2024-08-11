<template>
  <div class="h-full w-full">
    <div class="flex flex-col md:flex-row h-full w-full">
      <div class="w-full py-4 lg:py-20 md:w-2/12 md:h-full md:mx-5">
          <div v-if="!isMobile" class="flex flex-col gap-5 p-2 h-full w-full text-left p-5">
            <p class="text-2xl text-theme-5 border-b-2 border-theme-5/75">管理</p>
            <AdminMenu v-model="mode"/>
          </div>
          <MobileAdminMenu v-if="isMobile" v-model="mode" />
      </div>
      <div class="w-auto md:w-10/12 flex flex-col gap-10 overflow-y-scroll mt-5">
        <p class="text-theme-5 text-left text-4xl hidden md:inline">{{ {blog: "博客", file: "文件"}[mode] }}</p>
        <div ref="body" class="w-full h-full relative">
          <AdminBlogManagement v-if="mode == 'blog'" />
          <AdminFileManagement v-if="mode == 'file'" />
          <AdminBlogTagManagement v-if="mode == 'blog-tag'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AdminBlogManagement from '@/components/admin/AdminBlogManagement.vue';
import AdminBlogTagManagement from '@/components/admin/AdminBlogTagManagement.vue';
import AdminFileManagement from '@/components/admin/AdminFileManagement.vue';
import AdminMenu from '@/components/admin/AdminMenu.vue';
import MobileAdminMenu from '@/components/admin/MobileAdminMenu.vue';
import { isMobile } from '@/utils';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const mode = ref("blog")
const body = ref()

</script>

<style scoped>
::-webkit-scrollbar {
  display: none;
}
</style>
