<template>
  <div class="flex flex-column post gap-1">
    <Card>
      <template #title>
        <div class="flex author gap-3">
          <Avatar :image="author.avatar" shape="circle" />
          <p class="flex text-color align-items-center author-name">{{ author.nickname }}</p>
          <p class="flex align-items-center information">{{ `#${props.post.id} ${time}` }}</p>
          
        </div>
      </template>
      <template #content>
        <div class="flex content">
          <p class="text-color">{{ post.content }}</p>
        </div>
        <div class="flex interaction gap-2">
          <Button :icon='liked ? "pi pi-thumbs-up-fill" : "pi pi-thumbs-up"' @click="onLike" text />
          <Button :icon='showComments ? "pi pi-eye-slash" : "pi pi-eye"' :label='showComments ? "隐藏评论" : "显示评论"' @click="onShowComments" text />
          <div class="flex flex-row other-likes">
            <p>{{ likes.length == 0 ? "暂无人点赞" : "点赞：" }}</p>
            <AvatarGroup v-if="likes.length != 0">
              <Avatar v-for="user in likes" :key="user.id" :image="user.avatar" shape="circle" :title="user.nickname"/>
              <Avatar v-if="likesCount > MAX_DISPLAY_LIKES" :label="'+'+(likesCount - MAX_DISPLAY_LIKES)" shape="circle"></Avatar>
            </AvatarGroup>
          </div>
        </div>
        <div class="flex comments" v-if="showComments">
          <ActivityComment :comments="comments" :owner-id="post.id"></ActivityComment> 
        </div>
      </template>
    </Card>
    
  </div>
</template>

<script setup>
import { computed, ref, watch, defineProps, provide } from 'vue'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar';
import AvatarGroup from 'primevue/avatargroup';
import Card from 'primevue/card';
import ActivityComment from './ActivityComment.vue';
import { useUserStore } from '@/stores/users';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';
import { toastError, toastSuccess } from '@/utils';
import { formatActivityDate } from './ActivityUtils';

const MAX_DISPLAY_LIKES = 3

const toast = useToast()
const userStore = useUserStore()

const props = defineProps(["post"])
const post = ref(props.post)
const time = computed(() => formatActivityDate(new Date(post.value.time)))

const rawComments = ref([])
const comments = ref([])

const liked = ref(false)
userStore.getCurrentUser().then((user) => liked.value = post.value.likes.includes(user.id))
const showComments = ref(false)

const author = ref({})
userStore.getuser(post.value.author).then((user) => author.value = user)

const likes = ref([])
const likesCount = computed(() => {
  if (post.value) {
    return post.value.likes.length
  }
  return 0
})

const refreshRawComments = () => {
  var result = new Map();
  
  rawComments.value.forEach((comment) => {
    if (comment.father_comment == null) { //代表这个是最外层的评论
      result.set(comment.id, comment)
      comment.subComments = undefined
    } else { // 楼中楼
      var father = result.get(comment.father_comment) // 找到他的父评论，根据时间顺序，理论上父评论的记录肯定在子评论前
      if (father.subComments != undefined) { // 加入父评论
        father.subComments.push(comment) 
      } else {
        father.subComments = [comment]
      }
    }
  })
  comments.value = [...result.values()];
}

// 给评论输入的子组件用，方便输入之后直接刷新
const pushRawComment = (rawComment) => {
  rawComments.value.push(rawComment)
  refreshRawComments()
  
}
provide('push-raw-comment', pushRawComment)

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
    refreshLikes()
  })
}

const onShowComments = () => {
  showComments.value = !showComments.value
}

const refreshComments = () => {
  axios.get("/api/activity/comments/list_by_owner/", { params: { owner: post.value.id } }).then((resp) => {
    rawComments.value = resp.data;
    refreshRawComments()
  })
}

const refreshLikes = async () => {
  likes.value = await Promise.all(post.value.likes.slice(0, MAX_DISPLAY_LIKES).map(async id => (await userStore.getuser(id))))
}

refreshLikes()
watch(post, refreshComments)
refreshComments()

</script>

<style scoped>
.post {
  padding-left: 1rem;
  width: 100%;
}
.information {
  margin: 0;
  margin-left: auto; 
  margin-right: 1em;
  font-size: 0.9rem;
  color: var(--surface-400);
}
.author-name {
  margin: 0;
  padding: 0;
  font-size: 1.2rem;
  line-height: 0;
}
.content p {
  text-align: left;
}
.other-likes {
  font-size: 0.8rem;
  color: var(--surface-400);
  margin-left: auto;
}
.comments {
  margin-left: 1.5rem;
}
</style>
