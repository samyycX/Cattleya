<template>
  <div>
    <div class="flex flex-col gap-8 text-theme-5 h-max overflow-x-visible">
      <div v-for="blog in blogs" :key="blog.id" class="flex flex-row gap-5 h-max text-xs md:text-md">
        <div class="flex flex-col gap-0 justify-between grow">
          <div class="w-full flex flex-row justify-between">
            <p class="text-2xl cursor-pointer underline md:no-underline hover:underline underline-offset-4 text-theme-8" @click="() => toBlog(blog.id)">{{ blog.title }}</p>
            <p class="leading-none my-auto text-sm md:text-lg">{{ new Date(blog.created_time).toDateString() }}</p>
          </div>
          <div class="w-full flex flex-row gap-2 text-center text-theme-5/80">
            <ArrowPathIcon class="size-3 my-auto" />
            <p class="leading-none text-xs md:text-sm">{{ getLastUpdatedInterval(blog.updated_time) }} AGO</p>
          </div>
          <div class="w-full flex flex-row text-theme-5/80 text-sm md:text-md">
            <p class="hover:underline underline-offset-4 cursor-pointer hover:text-theme-5">{{ blog.author.nickname }}</p>
            <p class="ml-5">共 {{ blog.length }} 字</p>
            <p class="text-sm text-theme-5/80 my-auto leading-none ml-5" hidden>#{{ blog.id }}</p>
            <div class="ml-auto flex flex-row gap-2">
              <div v-for="tag in blog.tags" :key="tag.id" class="flex flex-row text-xs md:text-md">
                <p class="underline underline-offset-4 cursor-pointer hover:text-theme-5" @click="() => toBlogTag(tag)">#{{ tag.name }}</p>
              </div>
            </div>
            <div class="ml-auto" v-if="blog.tags.length == 0">
              <p class="text-theme-5/80">此文章暂无标签</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ArrowPathIcon } from '@heroicons/vue/24/outline';
import { defineProps, defineModel } from 'vue';
import { useRouter } from 'vue-router';

const blogs = defineModel()
const props = defineProps(["isAdmin"])
const router = useRouter();

const getLastUpdatedInterval = (time) => {

var interval = new Date() - new Date(time);
if (interval < 1000 * 60 * 60) {
  return `${parseInt(interval/(1000*60))}MIN`
} else if (interval < 1000 * 60 * 60 * 24) {
  return `${parseInt(interval/(1000*60*60))}HOUR`
} else {
  return `${parseInt(interval/(1000*60*60*24))}DAY`
}
};
const toBlog = (id) => {
  router.push({ path: `/blog/${id}` });
}
const toBlogTag = (tag) => {
  window.location.href = `/blog/list?tag=${tag.id}`;
}

</script>
