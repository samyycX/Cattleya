<template>
  <div class="flex align-items-center">
    <div class="flex flex-column align-items-center gap-6 border-round posts">
      <ActivityPost class="flex" v-for="post in posts" :key="post.id" :post="post"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ActivityPost from '@/components/activity/ActivityPost.vue';
import axios from 'axios';

// // 模拟生成从接口返回的comment
// const generateComment = (id, fatherCommentId, content) => {
//   return {
//     id: id,
//     author: user,
//     content: content,
//     time: Date.now(),
//     fatherCommentId: fatherCommentId, // 楼中楼，层主的id
//     ownerId: 0 // 帖子的id
//   }
// } 

// // 包含所有raw comment的列表，响应式，用户请求新的就往里面加
// // eslint-disable-next-line
// const rawComments = ref([
//   generateComment(0, null, "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."),
//   generateComment(1, 0, "楼中楼1"),
//   generateComment(2, 0, "楼中楼2"),
//   generateComment(3, 0, "楼中楼3"),
//   generateComment(4, null, "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."),
//   generateComment(5, null, "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."),
//   ...[...Array(10).keys()].map((k) => generateComment(k+5+1, 0, `楼中楼${k+5+1}`)),
//   ...[...Array(10).keys()].map((k) => generateComment(k+15+1, null, "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."))
// ])

// const post = {
//   id: 0,
//   author: {
//     avatar: require("@/assets/test_avatar.jpg"),
//     name: "测试用户"
//   },
//   time: Date.now(),
//   content: "Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis.",
//   likes: ["测试用户2", "测试用户3"],
//   comments: rawComments // TODO: 这里的comments应该是不存在的，由子组件自行根据ID去请求api
// }

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
    
    console.log(data.results)
    posts.value = posts.value.concat(data.results)
    if (data.next == null) {
      noMore = true;
    }
  }).finally(() => {
    page += 1
    getPostsLock = false
  })
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
