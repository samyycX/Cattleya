<template>
  <div class="flex flex-row gap-4">
    <InputText class="flex flex-grow-1" type="text" v-model="comment"></InputText>
    <Button class="flex" icon="pi pi-check" label="提交" @click="confirmSubmit"></Button>
  </div>
</template>

<script setup>
import { ref, defineProps, inject, defineEmits } from 'vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import { useConfirm } from "primevue/useconfirm";
import { useToast } from 'primevue/usetoast';
import axios from 'axios';

const confirm = useConfirm();
const toast = useToast();

const comment = ref(null)
const pushRawComment = inject('push-raw-comment')
const emit = defineEmits(['goto-last-page'])

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
  const body = {
    content: comment.value,
    father_comment: props.fatherCommentId,
    owner: props.ownerId,
  }
  axios.post("/api/activity/comments/", body).then((resp) => {
    const result = resp.data;
    if (result.code == 201) {
      toast.add({ severity: 'success', summary: "ξ( ✿＞◡❛)", detail: "回复成功~", life: 3000 })
      comment.value = null;
      pushRawComment(result.data)
      emit('goto-last-page')
    } else {
      toast.add({ severity: 'error', summary: result.msg, life: 3000})
    }
  })
}
const confirmSubmit = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: "确定要提交吗？",
        icon: 'pi pi-exclamation-circle',
        rejectLabel: "取消",
        rejectIcon: 'pi pi-times',
        reject: () => {},
        acceptLabel: "确定！",
        acceptIcon: 'pi pi-check',
        accept: submit
    })
}
</script>
