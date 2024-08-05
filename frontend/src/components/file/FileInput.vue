<template>
  <div>
    <input type="file" id="upload" @change="onUploaded" hidden/>  
  </div>
</template>

<script setup>

import { useNotification } from '@/stores/notifications';
import { defineExpose, defineProps, defineEmits } from 'vue';
import axios from 'axios';

const props = defineProps(["allowMultiple", "notify"])
const emit = defineEmits(["success", "fail"])

const notification = useNotification()

const callUpload = () => {
  document.getElementById("upload").click()
}

const upload = (files) => {
  onUploaded({ target: { files } })
}

defineExpose({ callUpload, upload })

const onUploaded = ({ target }) => {
  var files = null;
  files = props.allowMultiple ? target.files : [target.files[0]]

  const formData = new FormData();
  for (var file of files) {
    formData.append("files", file);
  }
  axios.post("/api/files/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(resp => {
    var result = resp.data;
    if (result.code == 201) {
      var data = result.data
      emit("success", data)
      if (props.notify) {
        notification.success(result.msg)
      }
    } else {
      emit("fail")
      if (props.notify) {
        notification.error(result.msg)
      }
    }
  });
}
</script>
