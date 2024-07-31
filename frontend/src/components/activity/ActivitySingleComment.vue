<template>
  <div class="flex flex-row comment">
    <Avatar :image="author.avatar" shape="circle"/>
    <div class="flex flex-column gap-1 right">
      <p class="flex justify-content-start author-name">{{ author.nickname }}</p>
      <p class="flex content">{{ props.comment.content }}</p>
      <div class="flex flex-row align-items-center gap-2">
        <p class="flex information align-items-center justify-content-center">{{ `#${props.index} ${time}` }}</p>
        <Button class="flex replybutton" label="回复" link @click="onReplyButtonClicked"/>
      </div>
      <div class="flex reply" v-if="showReply">
        <ActivityCommentInput :father-comment-id="props.comment.id" :owner-id="props.ownerId" @goto-last-page="gotoLastPage"/>
      </div>
      <div class="flex flex-column gap-2" v-if="props.comment.subComments" @wheel="onWheel">
        <div class="flex" v-for="(comment, i) in props.comment.subComments.slice(first, first+rows)" :key="comment.id">
          <ActivitySingleSubComment class="flex" :comment="comment" :index="first+i+1" :owner-id="props.ownerId"></ActivitySingleSubComment>
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
import { defineProps, computed, ref, defineEmits } from 'vue';
import ActivitySingleSubComment from "./ActivitySingleSubComment.vue"
import Button from 'primevue/button';
import ActivityCommentInput from './ActivityCommentInput.vue';
import Paginator from 'primevue/paginator';
import Avatar from 'primevue/avatar';
import { useUserStore } from '@/stores/users';
import { formatActivityDate } from './ActivityUtils';

const props = defineProps({
  comment: {
    type: Object,
    required: true,
  },
  ownerId: {
    type: Number,
    required: true
  },
  index: {
    type: Number,
    required: true,
  }
});
const emit = defineEmits(['cancel-next-wheel'])
const userStore = useUserStore()
const author = ref({})
userStore.getuser(props.comment.author).then((user) => author.value = user)
const time = computed(() => formatActivityDate(new Date(props.comment.time)))

const first = ref(0); // 分页器控制的初始index
const rows = 3; // 分页行数
const showReply = ref(false);

const onReplyButtonClicked = () => {
  showReply.value = !showReply.value;
}

const gotoLastPage = () => {
  first.value = parseInt(props.comment.subComments.length / rows) * rows
}
const gotoNextPage = () => {
  if (first.value + rows >= props.comment.subComments.length) {
    return
  }
  first.value += rows
}
const gotoPrevPage = () => {
  if (first.value - rows < 0) {
    return
  }
  first.value -= rows
}

const onWheel = (e) => {
  if (e.wheelDeltaY > 0) {
    e.preventDefault()
    gotoPrevPage()
    emit('cancel-next-wheel')
  } else if (e.wheelDeltaY < 0) {
    e.preventDefault()
    gotoNextPage()
    emit('cancel-next-wheel')
  }
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
  color: var(--surface-400);
}
.content {
  margin: 0;
  margin-top: 0.6rem;
  text-align: left;
  color: var(--text-color);
}
.information {
  margin: 0;
  font-size: 0.75rem;
  color: var(--surface-400);
}
.replybutton {
  font-size: 0.75rem;
}
.reply {
  transform: scale(0.8);
  transform-origin: 0;
}
</style>
