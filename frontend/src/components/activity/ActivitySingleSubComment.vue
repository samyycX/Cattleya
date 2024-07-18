<template>
  <div class="flex flex-row comment gap-2">
   <img class="flex avatar border-round" :src="props.comment.author.avatar" />
   <div class="flex flex-column">
    <div class="flex flex-row gap-3 right">
     <p class="flex align-items-start flex-nowrap author-name">{{ props.comment.author.name }}</p>
     <p class="flex align-items-start content">{{ props.comment.content }}</p>
    </div>
    <div class="flex flex-row align-items-center gap-2">
     <p class="flex time align-items-center justify-content-center p-text-secondary">{{ time }}</p>
     <Button class="flex replybutton" label="回复" link @click="onReplyButtonClicked"/>
    </div>
    <div class="flex reply" v-if="showReply">
     <ActivityCommentInput :father-comment-id="props.comment.id" :owner-id="props.ownerId"/>
    </div>
   </div>
  </div> 
</template>

<script setup>
import { defineProps, computed, ref } from 'vue';
import Button from 'primevue/button';
import ActivityCommentInput from './ActivityCommentInput.vue';
const props = defineProps({
 comment: {
  type: Object,
  required: true
 },
 ownerId: {
  type: Number,
  required: true
 }
});

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
 width: 1.5rem;
 height: 1.5rem;
}
.author-name {
  margin: 0;
  text-wrap: nowrap;
  color: var(--text-color);
  font-size: 0.9rem;
}
.content {
 margin: 0;
 text-align: left;
 color: var(--text-color);
 font-size: 0.9rem;
 justify-content: center;
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
