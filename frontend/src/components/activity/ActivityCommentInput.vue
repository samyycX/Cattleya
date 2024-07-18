<template>
  <div class="flex flex-row gap-4">
    <InputText class="flex flex-grow-1" type="text" v-model="comment"></InputText>
    <Button class="flex" icon="pi pi-check" label="提交" @click="submit"></Button>
    <Dialog v-model:visible="showCommentDialog" modal header="验证" style="width: 25rem">
      <p class="p-text-secondary">确定要评论吗？</p>
      <template #footer>
        <Button icon="pi pi-times" severity="secondary" label="我再想想" @click="onCommentDialogCancel" />
        <Button icon="pi pi-check" label="确定" @click="onCommentDialogCheck"/> <!-- TODO: 这里用`:loading:"loading"`加一个动画-->
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';

const comment = ref(null)
const showCommentDialog = ref(null)

// eslint-disable-next-line
const props = defineProps({
  fatherCommentId: { // 回复某回复的id，因为可能是直接回复帖子的所以required是false
    type: Number,
    required: false
  },
  ownerId: { // 帖子的ID
    type: Number,
    required: true
  }
}) 

const submit = () => {
  // TODO: 提交
  showCommentDialog.value = true;
}

const onCommentDialogCancel = () => {
  showCommentDialog.value = false;
}
const onCommentDialogCheck = () => {
  comment.value = null;
  showCommentDialog.value = false;
}
</script>
