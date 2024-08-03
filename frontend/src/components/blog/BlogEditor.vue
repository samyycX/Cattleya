<template>
  <div ref="editor" class="input-box" contenteditable="plaintext-only" @input="inputText" @blur="inputBlur" @focus="inputFocus">
    <div></div>
  </div>
</template>

<script setup>
import { watchEffect } from 'vue';
import { defineProps, defineEmits, ref } from 'vue';
const props = defineProps(["value"]);
const emit = defineEmits(["input"])
const editor = ref(null)
const isBlur = ref(false)

watchEffect(() => {
  if (isBlur.value && editor.value) {
    editor.value.innerText = props.value;
  }
})

const inputText = () => {
  emit("input", editor.value.innerText)
}

const inputFocus = () => {
  isBlur.value = false;
}

const inputBlur = () => {
  isBlur.value = true;
}

</script>
