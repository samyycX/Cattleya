<template>
 <div class="flex flex-column gap-3 comments flex-grow-1">
  <div class="flex">
   <ActivityCommentInput class="flex flex-grow-1" :owner-id="props.ownerId" @goto-last-page="gotoLastPage"/>
  </div>
  <div @wheel="onWheel">
    <div class="flex" v-for="(comment, i) in props.comments.slice(first, first+rows)" :key="comment.id">
      <ActivitySingleComment class="flex" :comment="comment" :index="first+i+1" :owner-id="props.ownerId" @cancel-next-wheel="cancelNextWheel"/>
    </div> 
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
var nextWheelCanceled = false

const gotoLastPage = () => {
  first.value = parseInt(props.comments.length / rows) * rows
}
const gotoNextPage = () => {
  if (first.value + rows >= props.comments.length) {
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

const cancelNextWheel = () => {
  nextWheelCanceled = true
}

const onWheel = (e) => {
  if (nextWheelCanceled) {
    nextWheelCanceled = false
    return
  }
  if (e.wheelDeltaY > 0) {
    e.preventDefault()
    gotoPrevPage()
  } else if (e.wheelDeltaY < 0) {
    e.preventDefault()
    gotoNextPage()
  }
}

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
