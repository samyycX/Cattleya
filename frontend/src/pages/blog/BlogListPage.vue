<template>
  <div class="h-full py-2 lg:py-16">
    <div class="h-full w-full">
      <div class="flex flex-row h-full">
        <div class="flex flex-col gap-8 w-full md:w-8/12 h-full overflow-y-scroll">
          <div class="flex flex-row gap-2 text-3xl text-left text-theme-5 border-b-2 border-theme-5 w-full" v-if="queriedTag != null">
            <HashtagIcon  class="size-8"/>
            <p>{{ queriedTag.name }}</p> 
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
import { ref } from 'vue';
import { isMobile } from '@/utils'
import BlogList from '@/components/blog/BlogList.vue'
import BlogTagCapsuleList from '@/components/blog/tag/BlogTagCapsuleList.vue';
import { HashtagIcon } from '@heroicons/vue/24/solid';

const route = useRoute()
const blogs = ref(route.meta.blogs)
const tags = ref(route.meta.tags)
const queriedTag = ref(route.meta.queriedTag)

</script>

<style scoped>
::-webkit-scrollbar {
  display:none
}
</style>
