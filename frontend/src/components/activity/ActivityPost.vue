<template>
  <div class="flex flex-column post gap-1">
    <Card>
      <template #title>
        <div class="flex author">
          <Avatar :image="author.avatar" shape="circle" />
          <p class="flex text-color align-items-center author-name">{{ author.nickname }}</p>
          <p class="flex align-items-center time">{{ nowGmtTime }}</p>
          
        </div>
      </template>
      <template #content>
        <div class="flex content">
          <p class="text-color">{{ post.content }}</p>
        </div>
        <div class="flex interaction gap-2">
          <Button :icon='liked ? "pi pi-thumbs-up-fill" : "pi pi-thumbs-up"' @click="onLike" text />
          <Button :icon='showComments ? "pi pi-eye-slash" : "pi pi-eye"' :label='showComments ? "隐藏评论" : "显示评论"' @click="onShowComments" text />
          <p v-if="post.likes.length != 0" class="flex other-likes p-text-secondary">{{ likesName + " 赞了" }}</p>
        </div>
        <div class="flex comments" v-if="showComments">
          <ActivityComment :comments="comments" :owner-id="post.id"></ActivityComment> 
        </div>
      </template>
    </Card>
    
  </div>
</template>

<script setup>
import { computed, ref, watch, defineProps } from 'vue'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar';
import Card from 'primevue/card';
import ActivityComment from './ActivityComment.vue';
import { useUserStore } from '@/stores/users';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';
import { toastError, toastSuccess } from '@/utils';

const toast = useToast()
const userStore = useUserStore()

const props = defineProps(["post"])
const post = ref(props.post)
const rawComments = ref([])
const comments = ref([])
const likesName = ref([])

const author = ref({})

userStore.getuser(post.value.author).then((user) => author.value = user)


watch(rawComments,
(newRawComments, oldRawComments) => { // 从数据记录构造评论树
  if (oldRawComments != undefined && oldRawComments.length == newRawComments.length) { // 避免不必要的更新
    return;
  }
  var result = new Map();
  
  newRawComments.forEach((comment) => {
    if (comment.father_comment_id == null) { //代表这个是最外层的评论
      result.set(comment.id, comment)
    } else { // 楼中楼
      var father = result.get(comment.father_comment_id) // 找到他的父评论，根据时间顺序，理论上父评论的记录肯定在子评论前
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
  return `${date.getFullYear()}年${date.getMonth()+1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`
})

const liked = ref(false)
userStore.getCurrentUser().then((user) => liked.value = post.value.likes.includes(user.id))
var showComments = ref(false)
const onLike = () => {
  axios.post(`/api/activity/posts/${post.value.id}/like/`).then((resp) => {
    const result = resp.data;
    if (result.code == 200) {
      toastSuccess(toast, result.msg)
      liked.value = result.data
      var id = userStore.currentUser.id
      if (result.data) {
        post.value.likes.push(id)
      } else {
        post.value.likes.splice(post.value.likes.indexOf(id))
      }
    } else {
      toastError(toast, result.msg)
    }
  }).finally(() => {
    refreshLikesName()
  })
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

const refreshLikesName = async () => {
  likesName.value = await Promise.all(post.value.likes.map(async id => (await userStore.getuser(id)).nickname))
}

refreshLikesName()
watch(post, refreshComments)
refreshComments()

</script>

<style scoped>
.post {
  padding-left: 1rem;
  width: 100%;
}
.time {
  margin: 0;
  margin-left: auto; 
  margin-right: 1em;
  font-size: 0.9rem;
  color: var(--surface-400);
}
.author-name {
  margin: 0;
  margin-left: 1rem;
  padding: 0;
  font-size: 1.2rem;
  line-height: 0;
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
