<template>
  <div class="flex flex-col">
     <div class="flex flex-col w-1/6">
        <img class="rounded-xl" :src="author.avatar" />
        <span>{{ author.nickname }}</span>
     </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/users';
import { defineProps, ref, watchEffect } from 'vue';
import axios from 'axios';
const userStore = useUserStore();

const props = defineProps(["post"])
// const post = ref(props.post)
const post = ref({})
axios.get("/api/activity/posts/1/").then((resp) => post.value = resp.data);


const author = ref({})

watchEffect(() => {
  userStore.getuser(post.value.author).then((user) => author.value = user);
})

</script>

<style scoped>
  
</style>
