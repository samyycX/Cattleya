<template>
  <div class="h-full py-2 lg:py-16">
    <div class="h-full w-full">
      <div class="flex flex-row h-full">
        <div class="flex flex-col gap-8 w-full md:w-8/12 h-full overflow-y-scroll">
          <div class="flex flex-row gap-2 text-3xl text-left text-theme-5 border-b-2 border-theme-5 w-full" v-if="queriedTag != null">
            <HashtagIcon  class="size-8"/>
            <p>{{ queriedTagName }}</p> 
          </div>
          <BlogList v-model="blogs" class="pb-0 md:pb-16 lg:pb-0" />
        </div>
        <div class="flex flex-col w-4/12 px-3 lg:px-16" v-if="!isMobile">
          <BlogTagCapsuleList :tags="tags"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { onBeforeMount, ref } from 'vue';
import { isMobile } from '@/utils'
import BlogList from '@/components/blog/BlogList.vue'
import BlogTagCapsuleList from '@/components/blog/tag/BlogTagCapsuleList.vue';
import { HashtagIcon } from '@heroicons/vue/24/solid';
import axios from 'axios';
import { useNotification } from '@/stores/notifications';

const BLOG_LIMIT = 10

const route = useRoute()
const queriedTag = ref(route.query.tag)
const queriedTagName = ref()
const blogs = ref([])
const tags = ref()

const blogHasNext = ref(true)
const blogNextOffset = ref(0)

const notification = useNotification()

const fetchMoreBlog = () => {
  let params = {
    offset: blogNextOffset.value,
    limit: BLOG_LIMIT
  };
  if (queriedTag.value) {
    params.tag = parseInt(queriedTag.value);
  }
  axios.get("/api/blogs/listBriefByLatest/", { params }).then((resp) => {
    const result = resp.data;
    if (result.code != 200) {
      notification.error(result.msg);
    } else {
      blogs.value.push(...result.data.results);
      blogHasNext.value = result.next != null;
      blogNextOffset.value += BLOG_LIMIT;
    }
  });
}

onBeforeMount(() => {
  fetchMoreBlog()
  if (queriedTag.value) {
    axios.get(`/api/blog-tags/${queriedTag.value}/`).then((resp) => {
      const result = resp.data;
      if (result.code != 200) {
        notification.error(result.msg);
      } else {
        queriedTagName.value = result.data.name;
      }
    });
  }
 
  axios.get("/api/blog-tags/").then((resp) => {
    const result = resp.data;
    if (result.code != 200) {
      notification.error(result.msg);
    } else {
      tags.value = result.data;
    }
  });
})

</script>

<style scoped>
::-webkit-scrollbar {
  display:none
}
</style>
