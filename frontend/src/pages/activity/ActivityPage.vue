<template>
  <div class="flex align-items-center">
    <div class="flex flex-column align-items-center gap-6 border-round posts">
      <ActivityPostInput @add-post="addPost" />
      <ActivityPost class="flex" v-for="post in posts" :key="post.id" :post="post"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ActivityPost from '@/components/activity/ActivityPost.vue';
import axios from 'axios';
import ActivityPostInput from '@/components/activity/ActivityPostInput.vue';

const posts = ref([])

var page = 1
var noMore = false
var getPostsLock = false;

const getPosts = () => {
  if (getPostsLock) {
    return;
  }
  getPostsLock = true;
  axios.get("/api/activity/posts/", {
    params: {
      page,
    }
  }).then(async (resp) => {
    const data = resp.data; 
    posts.value = posts.value.concat(data.results)
    if (data.next == null) {
      noMore = true;
    }
  }).finally(() => {
    page += 1
    getPostsLock = false
  })
}

const addPost = (post) => {
  posts.value.splice(0, 0, post)
} 

// 滚动到底的时候刷新
window.onscroll = () => {
  var windowHeight = document.documentElement.clientHeight || document.body.clientHeight;
	var documentHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
	var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;

  if ((windowHeight + scrollTop + 2) >= documentHeight && !noMore){
    getPosts()
  }
}
getPosts()

</script>

<style scoped>
.posts {
  width: 70%;
  border: 1px solid var(--primary-color);
  border-top: 0;
}
</style>
