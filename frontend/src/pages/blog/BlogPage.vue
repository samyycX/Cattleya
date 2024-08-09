<template>
  <div class="flex flex-row">
    <div id="blog-scrollable-container" class="flex flex-col gap-2 px-2 md:px-0 w-full text-left md:w-9/12 md:px-12 pt-7 mx-auto max-w-none prose prose-cattleya prose-md lg:prose-xl text-left bg-theme-0 h-max md:h-screen md:overflow-y-scroll overflow-x-hidden" @scroll="onScroll">
      <div class="flex flex-col gap-3">
        <p class="!my-0 text-theme-5/80 text-sm">{{ new Date(blog.created_time).toDateString() }}</p>
        <h1 id="blog-title" class="!mb-0">{{ blog.title }}</h1>
        <div class="flex flex-row flex-wrap gap-3 !my-0 text-theme-5/80 w-full text-left text-sm !leading-none">
          <p class="!my-0">#{{ blog.id }}</p>
          <p class="!my-0">|</p>
          <div class="flex flex-row !my-0">
            <PencilSquareIcon class="size-4 !my-0" />
            <p class="leading-none !my-0 ml-1 cursor-pointer hover:text-theme-5">{{ blog.author.nickname }}</p>
          </div>
          <p class="!my-0">|</p>
          <p class="!my-0">共 {{ blog.length }} 字</p>
          <p class="!my-0">|</p>
          <p class="!my-0">{{ getLastUpdatedInterval(blog.updated_time) }} 前更新</p>
        </div>
      </div>
      <BlogMdxRender :content="blog.content" @render-complete="bindDoms"/>  
    </div>
    <div class="w-3/12 h-screen mt-16 overflow-y-scroll lg:overflow-y-hidden pb-48 lg:pb-4" v-if="!isMobile">
      <div class="flex flex-col gap-20 h-max lg:h-[90%]">
        <BlogDirectory ref="directory" :content="blog.content" :title="blog.title" />
        <BlogTagCapsuleList :tags="blog.tags"/>
        <div class="mt-auto">
          <div class="flex flex-row gap-2 text-theme-5 border-b-[1.5px] border-transparent hover:border-theme-5 cursor-pointer w-fit" @click="backToTop">
            <ArrowUpIcon class="size-4 my-auto" />
            <p>回到顶部</p>
          </div>
        </div>
      </div>
    </div>
    <div class="fixed flex flex-col right-4 bottom-4" v-if="isMobile">
      <div class="rounded-md border-2 border-theme-5 bg-theme-0" @click="backToTop">
        <ArrowUpIcon class="size-8 text-theme-5" />
      </div>
    </div>
  </div>
</template>

<script setup lang="jsx">
import BlogDirectory from '@/components/blog/BlogDirectory.vue';
import BlogMdxRender from '@/components/blog/BlogMdxRender.vue';
import BlogTagCapsuleList from '@/components/blog/tag/BlogTagCapsuleList.vue';
import { isMobile } from '@/utils';
import { PencilSquareIcon, ArrowUpIcon } from '@heroicons/vue/24/outline';

import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const blog = ref(route.meta.blog);

const directory = ref()

const getLastUpdatedInterval = (time) => {
  var interval = new Date() - new Date(time);
  if (interval < 1000 * 60 * 60) {
    return `${parseInt(interval/(1000*60))}分钟`
  } else if (interval < 1000 * 60 * 60 * 24) {
    return `${parseInt(interval/(1000*60*60))}小时`
  } else {
    return `${parseInt(interval/(1000*60*60*24))}日`
  }
};

const bindDoms = () => {
  if (directory.value == undefined) {
    return;
  } 
  setTimeout(() => {
    var title = [document.getElementById("blog-title")];
    var content = Array.from(document.getElementById("mdx-content-container").children);
    directory.value.startBindDoms(Array.prototype.concat(title, content))
  }, 100)
}

const onScroll = (e) => {
  if (directory.value == undefined) {
    return;
  } 
  directory.value.onScroll(e.target.scrollTop);
}

const backToTop = () => {
  if (!isMobile.value) {
    document.getElementById("blog-scrollable-container").scrollTop = 0;
    onScroll({ target: { scrollTop: 0} });
  } else {
    document.getElementById("body").scrollTop = 0;
  }
}

</script>

<style scoped>
::-webkit-scrollbar {
  display: none;
}

</style>
