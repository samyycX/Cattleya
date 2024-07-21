<template>
  <div class="flex flex-row comment">
   <Avatar :image="author.avatar" />
   <div class="flex flex-column gap-1 right">
    <p class="flex justify-content-start author-name">{{ author.nickname }}</p>
    <p class="flex content">{{ props.comment.content }}</p>
    <div class="flex flex-row align-items-center gap-2">
     <p class="flex time align-items-center justify-content-center p-text-secondary">{{ time }}</p>
     <Button class="flex replybutton" label="回复" link @click="onReplyButtonClicked"/>
    </div>
    <div class="flex reply" v-if="showReply">
     <ActivityCommentInput :father-comment-id="props.comment.id" :owner-id="props.ownerId" />
    </div>
    <div class="flex flex-column gap-2" v-if="props.comment.subComments">
    <div class="flex" v-for="comment in props.comment.subComments.slice(first, first+rows)" :key="comment.id">
     <ActivitySingleSubComment class="flex" :comment="comment" :owner-id="props.ownerId"></ActivitySingleSubComment>
    </div> 
    <Paginator
     class="flex"
     v-if="props.comment.subComments != undefined && props.comment.subComments.length > rows"
     v-model:first="first"
     :rows="rows"
     :total-records="props.comment.subComments.length"
    />
    </div>
   </div>
  </div> 
</template>

<script setup>
import { defineProps, computed, ref } from 'vue';
import ActivitySingleSubComment from "./ActivitySingleSubComment.vue"
import Button from 'primevue/button';
import ActivityCommentInput from './ActivityCommentInput.vue';
import Paginator from 'primevue/paginator';
import Avatar from 'primevue/avatar';
import { useUserStore } from '@/stores/users';

const props = defineProps({
 comment: {
  type: Object,
  required: true,
 },
 ownerId: {
  type: Number,
  required: true
 }
});

const userStore = useUserStore()
const author = ref({})
userStore.getuser(props.comment.author_id).then((user) => author.value = user)

const first = ref(0); // 分页器控制的初始index
const rows = 3; // 分页行数
const showReply = ref(false);
const time = computed(() => {
 var date = new Date(props.comment.time);
 return `${date.getFullYear()}年${date.getMonth()}月${date.getDay()}日 ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`
})

const onReplyButtonClicked = () => {
 showReply.value = !showReply.value;
}

</script>

<style scoped>
.avatar {
 width: 3.5rem;
 height: 3.5rem;
 border-radius: 1rem;
}
.right {
 margin-left: 1rem;
}
.author-name {
 margin: 0;
 color: var(--text-color);
}
.content {
 margin: 0;
 margin-top: 0.6rem;
 text-align: left;
 color: var(--text-color);
}
.time {
 margin: 0;
 font-size: 0.75rem;
}
.replybutton {
 font-size: 0.75rem;
}
.reply {
 transform: scale(0.8);
 transform-origin: 0;
}
</style>
