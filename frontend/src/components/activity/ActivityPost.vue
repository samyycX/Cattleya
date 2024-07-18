<template>
  <div class="flex flex-column post gap-1">
    <div class="flex author">
      <img class="flex avatar border-round" :src="post.author.avatar" />
      <p class="flex align-items-center">{{ post.author.name }}</p>
      <p class="flex align-items-center" style="margin-left: auto; margin-right: 1em">{{ nowGmtTime }}</p>
    </div>
    <div class="flex content">
      <p>{{ post.content }}</p>
    </div>
    <div class="flex interaction gap-2">
      <Button :icon='liked ? "pi pi-thumbs-up-fill" : "pi pi-thumbs-up"' @click="onLike" text/>
      <Button :icon='showComments ? "pi pi-eye-slash" : "pi pi-eye"' :label='showComments ? "隐藏评论" : "显示评论"' @click="onShowComments" text/>
      <p v-if="post.otherLikes.length != 0" class="flex other-likes p-text-secondary">{{ post.otherLikes.join(",") + " 赞了" }}</p>
    </div>
    <div class="flex comments" v-if="showComments">
      <ActivityComment :comments="post.comments" :owner-id="post.id"></ActivityComment> 
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import Button from 'primevue/button'
import ActivityComment from './ActivityComment.vue';

// 模拟用户
const user = {
  avatar: require("@/assets/test_avatar.jpg"),
  name: "samyyc"
}

// 模拟生成从接口返回的comment
const generateComment = (id, fatherCommentId, content) => {
  return {
    id: id,
    author: user,
    content: content,
    time: Date.now(),
    fatherCommentId: fatherCommentId, // 楼中楼，层主的id
    ownerId: 0 // 帖子的id
  }
} 

// 包含所有raw comment的列表，响应式，用户请求新的就往里面加
// eslint-disable-next-line
const rawComments = ref([
  generateComment(0, null, "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."),
  generateComment(1, 0, "楼中楼1"),
  generateComment(2, 0, "楼中楼2"),
  generateComment(3, 0, "楼中楼3"),
  generateComment(4, null, "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."),
  generateComment(5, null, "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."),
  ...[...Array(10).keys()].map((k) => generateComment(k+5+1, 0, `楼中楼${k+5+1}`)),
  ...[...Array(10).keys()].map((k) => generateComment(k+15+1, null, "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."))
])

const comments = ref([])


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
    comments.value = [...result.values()];
  },
  { immediate: true } // 立刻刷新
)

const post = ref({
  id: 0,
  author: {
    avatar: require("@/assets/test_avatar.jpg"),
    name: "测试用户"
  },
  time: Date.now(),
  content: "Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis.",
  likes: 666,
  otherLikes: ["测试用户2", "测试用户3"],
  comments: comments
})

const currentUser = "测试用户4"

const nowGmtTime = computed(() => {
  var date = new Date(post.value.time)
  return `${date.getFullYear()}年${date.getMonth()}月${date.getDay()}日 ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`
})
var liked = ref(false)
var showComments = ref(false)

const onLike = () => {
  if (liked.value) {
    post.value.likes -= 1
    post.value.otherLikes = post.value.otherLikes.filter((v) => v != currentUser)
  } else {
    post.value.likes += 1
    post.value.otherLikes.push(currentUser)
  }
  liked.value = !liked.value; 
}

const onShowComments = () => {
  showComments.value = !showComments.value
}

</script>

<style scoped>
.post {
  border: 2px solid black;
  padding-left: 1rem;
}
.avatar {
  width: 3.5rem;
  height: 3.5rem;
}
.author p {
  margin: 0;
  margin-left: 1rem;
  color: var(--text-color);
}
.content p {
  text-align: left;
  color: var(--text-color);
}
.other-likes {
  font-size: 0.9rem;
}
.comments {
  margin-left: 1.5rem;
}
</style>
