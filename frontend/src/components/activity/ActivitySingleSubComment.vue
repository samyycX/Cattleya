<template>
  <div class="flex flex-row comment gap-2">
   <Avatar shape="circle" :image="author.avatar" />
   <div class="flex flex-column gap-1">
    <div class="flex flex-row gap-3 right">
     <p class="flex align-items-start flex-nowrap author-name">{{ author.nickname }}</p>
     <p class="flex align-items-start content">{{ props.comment.content }}</p>
    </div>
    <div class="flex flex-row align-items-center gap-2">
     <p class="flex information align-items-center justify-content-center p-text-secondary">{{ `#${props.index} ${time}` }}</p>
    </div>
   </div>
  </div> 
</template>

<script setup>
import { defineProps, computed, ref } from 'vue';
import Avatar from 'primevue/avatar';
import { useUserStore } from '@/stores/users';
import { formatActivityDate } from './ActivityUtils';
const props = defineProps({
 comment: {
  type: Object,
  required: true
 },
 ownerId: {
  type: Number,
  required: true
 },
 index: {
  type: Number,
  required: true
 }
});
const userStore = useUserStore();
const author = ref({})
userStore.getuser(props.comment.author).then((user) => author.value = user)
const time = computed(() => formatActivityDate(new Date(props.comment.time)))
</script>

<style scoped>
.avatar {
 width: 1.5rem;
 height: 1.5rem;
}
.author-name {
  margin: 0;
  text-wrap: nowrap;
  font-size: 0.9rem;
  color: var(--surface-400);
}
.content {
 margin: 0;
 text-align: left;
 color: var(--text-color);
 font-size: 0.9rem;
 justify-content: center;
 padding: 0;
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
