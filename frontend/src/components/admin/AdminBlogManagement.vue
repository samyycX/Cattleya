<template>
  <div class="overflow-x-visible">
    <BlogList v-model="blogs" is-admin="true"/>
  </div>
</template>

<script setup>
import axios from 'axios';
import BlogList from '../blog/BlogList.vue';
import { onBeforeMount, ref } from 'vue';

const blogs = ref([])

onBeforeMount(() => {
  axios.get(`/api/blogs/?visible=all`).then((resp) => {
    blogs.value = resp.data.data;
  })
})

</script>
