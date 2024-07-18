<template>
 <div class="flex flex-column gap-3 comments flex-grow-1">
  <div class="flex">
   <ActivityCommentInput class="flex flex-grow-1" :owner-id="props.ownerId"/>
  </div>
  <div class="flex" v-for="comment in props.comments.slice(first, first+rows)" :key="comment.id">
   <ActivitySingleComment class="flex" :comment="comment" :owner-id="props.ownerId" />
  </div> 
   <Paginator
   class="flex"
   v-if="props.comments != undefined && props.comments.length > rows"
   v-model:first="first"
   :rows="rows"
   :total-records="props.comments.length"
   />
 </div> 
</template>
 
<script setup>
import { defineProps, ref } from "vue";

import ActivitySingleComment from "./ActivitySingleComment.vue"
import ActivityCommentInput from './ActivityCommentInput.vue'
import Paginator from "primevue/paginator";

const props = defineProps({
 comments: {
  type: Array, 
  required: true
 },
 ownerId: {
  type: Number,
  required: true
 }
})

const first = ref(0) // 分页器控制的初始index
const rows = 3 // 分页器行数

</script>

<style scoped>
.comments {
 padding-left: 0.7em;
 border-left: 2px;
 border-left-style: solid;
 border-left-color: var(--primary-color);
 transform: scale(0.95);
 transform-origin: left;
 left: 0;

}
</style>
