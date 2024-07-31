<template>
  <div class="flex w-full">
    <Card class="w-full">
      <template #content>
        <FloatLabel>
          <Textarea v-model="input" class="w-full" autoResize></Textarea>
          <label id="label">{{ labelText }}</label>
        </FloatLabel>
      </template>
      <template #footer>
        <div class="flex flex-row gap-2 buttons">
          <Button label="清空" severity="danger" @click="confirmClear"></Button>
          <Button label="发布" @click="confirmSubmit" :disabled="submitDisabled"></Button>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import Card from 'primevue/card';
import Textarea from 'primevue/textarea';
import FloatLabel from 'primevue/floatlabel';
import Button from 'primevue/button';
import { ref, watchEffect, defineEmits } from 'vue';
import { useConfirm } from 'primevue/useconfirm';
import axios from 'axios';
import { toastError, toastSuccess } from '@/utils';
import { useToast } from 'primevue/usetoast';

const MAX_CONTENT_SIZE = 300

const confirm = useConfirm()
const toast = useToast()
const emit = defineEmits(['add-post'])

const labelText = ref(`发表你的动态吧~最多${MAX_CONTENT_SIZE}字`)
const input = ref("")
const submitDisabled = ref(false)

watchEffect(() => {
  if (input.value.length != 0) {
    labelText.value = `${input.value.length} / ${MAX_CONTENT_SIZE}`
  } else {
    labelText.value = `发表你的动态吧~最多${MAX_CONTENT_SIZE}字`
  }
  
  var label = document.getElementById("label")
  if (input.value.length > MAX_CONTENT_SIZE) {
    label && (() => {label.style.color = 'red'})()
    submitDisabled.value = true
  } else {
    label && (() => {label.style.color = 'var(--floatlabel-color)'})()
    submitDisabled.value = false
  }
})

const submit = () => {
  axios.post("/api/activity/posts/", {
    'content': input.value
  }).then(resp => {
    const result = resp.data
    if (result.code == 201) {
      toastSuccess(toast, result.msg)
      clear()
      emit('add-post', result.data)
    } else {
      toastError(toast, result.msg)
    }
  })
}

const clear = () => {
  input.value = ""
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

const confirmClear = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: "确定要清空吗？",
        icon: 'pi pi-exclamation-circle',
        rejectLabel: "取消",
        rejectIcon: 'pi pi-times',
        reject: () => {},
        acceptLabel: "确定！",
        acceptIcon: 'pi pi-check',
        accept: clear
    })
}
</script>

<style scoped>
.buttons {
  float: right;
}

</style>