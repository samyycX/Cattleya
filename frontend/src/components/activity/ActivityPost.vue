<template>
  <div class="flex flex-column post gap-1">
    <div class="flex author">
      <Avatar :image="author.avatar" rounded />
      <p class="flex text-color align-items-center">{{ author.nickname }}</p>
      <p class="flex text-color align-items-center" style="margin-left: auto; margin-right: 1em">{{ nowGmtTime }}</p>
    </div>
    <div class="flex content">
      <p class="text-color">{{ post.content }}</p>
    </div>
    <div class="flex interaction gap-2">
      <Button :icon='liked ? "pi pi-thumbs-up-fill" : "pi pi-thumbs-up"' @click="onLike" text />
      <Button :icon='showComments ? "pi pi-eye-slash" : "pi pi-eye"' :label='showComments ? "隐藏评论" : "显示评论"' @click="onShowComments" text />
      <p v-if="likes.length != 0" class="flex other-likes p-text-secondary">{{ likes.join(",") + " 赞了" }}</p>
    </div>
    <div class="flex comments" v-if="showComments">
      <ActivityComment :comments="comments" :owner-id="post.id"></ActivityComment> 
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, defineProps } from 'vue'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar';
import ActivityComment from './ActivityComment.vue';
import { useUserStore } from '@/stores/users';
import axios from 'axios';

const props = defineProps(["post"])
const rawComments = ref([])
const comments = ref([])

const userStore = useUserStore()
const post = ref(props.post)
const author = ref({})

userStore.getuser(post.value.author).then((user) => author.value = user)

const currentUser = ref()

axios.get("/api/user/info").then((resp) => {
  const result = resp.data;
  if (result.code == 200) {
    currentUser.value = result.data;
  }
})

watch(rawComments,
(newRawComments, oldRawComments) => { // 从数据记录构造评论树
  if (oldRawComments != undefined && oldRawComments.length == newRawComments.length) { // 避免不必要的更新
    return;
  }
  var result = new Map();
  
  newRawComments.forEach((comment) => {
    if (comment.fatherCommentId == null) { //代表这个是最外层的评论
      result.set(comment.id, comment)
    } else { // 楼中楼
      var father = result.get(comment.fatherCommentId) // 找到他的父评论，根据时间顺序，理论上父评论的记录肯定在子评论前
      if (father.subComments != undefined) { // 加入父评论
        father.subComments.push(comment) 
      } else {
        father.subComments = [comment]
      }
    }
  })
  console.log([...result.values()])
  comments.value = [...result.values()];
},
//{ immediate: true } // 立刻刷新
)

const nowGmtTime = computed(() => {
  var date = new Date(post.value.time)
  return `${date.getFullYear()}年${date.getMonth()}月${date.getDay()}日 ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`
})

var liked = ref(false)
var showComments = ref(false)
var likes = computed(() => {
  var likes = post.value.likes
  if (likes == undefined) {
    return []
  } else {
    return likes
  }
})
const onLike = () => {
  if (liked.value) {
    likes.value = likes.value.filter((v) => v != currentUser.value.id)
  } else {
    likes.value.push(currentUser.value.id)
  }
  liked.value = !liked.value; 
}

const onShowComments = () => {
  showComments.value = !showComments.value
}

const refreshComments = () => {
  axios.get("/api/activity/comment", { params: { owner: post.value.id } }).then((resp) => {
    const result = resp.data;
    if (result.code == 200) {
      rawComments.value = result.data;
    }
  })
}

watch(post, refreshComments)
refreshComments()

</script>

<style scoped>
.post {
  padding-left: 1rem;
  width: 100%;
}
.author p {
  margin: 0;
  margin-left: 1rem;
}
.content p {
  text-align: left;
}
.other-likes {
  font-size: 0.9rem;
}
.comments {
  margin-left: 1.5rem;
}
</style>
