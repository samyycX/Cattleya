<template>
  <div class="flex flex-col relative">
    <div class="border-2 border-theme-4 flex flex-row flex-wrap py-1">
      <div v-for="tag in selectedTags" :key="tag.id" class="flex flex-col mx-2 justify-center">
        <BlogSingleTag :name="tag.name" :cancelable="true" class="text-sm" @cancel="() => cancel(tag)"/>
      </div>
      <input type="text" class="outline-none bg-theme-0 pl-2" placeholder="输入以新建标签.." v-model="tagInput" @focus="onTagFocus" @blur="onTagBlur" />
    </div>
    <div v-if="showDropdown" class="absolute left-0 top-full border-theme-4 border-x-2 border-b-2 bg-theme-0 w-full h-[100px] flex flex-col pl-2 pt-2 overflow-y-scroll">
      <div class="hover:bg-theme-1 cursor-pointer" v-if="tagInput != '' && allTags.filter(t => t.name == tagInput).length == 0" @click="createTag">
        <p>新建标签：{{ tagInput }}</p>
      </div>
      <div v-for="tag in showedTags" :key="tag.id" class="hover:bg-theme-1 cursor-pointer" @click="() => select(tag)" @mousedown="preventLostFocus">
        <p>{{ tag.name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, defineExpose, computed, reactive } from 'vue';
import BlogSingleTag from './BlogSingleTag.vue';
import axios from 'axios';
import { useNotification } from '@/stores/notifications';

const notification = useNotification()

const allTags = ref([])
const showDropdown = ref(false)
const selectedTags = reactive([])
const showedTags = computed(() => allTags.value.filter(t => selectedTags.filter(t2 => t2.id == t.id).length == 0 && t.name.includes(tagInput.value)))
const tagInput = ref("")

defineExpose({ selectedTags })

onBeforeMount(async () => {
  allTags.value = (await axios.get("/api/blog-tags/")).data.data;
});

const select = (tag) => {
  selectedTags.push(tag);
}

const preventLostFocus = (e) => {
  e.preventDefault();
}

const cancel = (tag) => {
  selectedTags.splice(selectedTags.find(t => t.id != tag.id),1)
}

const createTag = () => {
  axios.post("/api/blog-tags/", {
    name: tagInput.value
  }).then(async (resp) => {
    const result = resp.data;
    if (result.code == 200) {
      allTags.value = (await axios.get("/api/blog-tags/")).data.data;
      selectedTags.push(result.data)
      tagInput.value = ""
    } else {
      notification.error(result.msg);
    }
  })
}

const onTagFocus = () => {
  showDropdown.value = true;
}

const onTagBlur = () => {
  showDropdown.value = false;
}


</script>

<style scoped>
::-webkit-scrollbar {
 /*高宽分别对应横竖滚动条的尺寸*/
  width: 10px;     
  height: 1px;
}

/*滚动条里面小方块*/
::-webkit-scrollbar-thumb {
 -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
  background: var(--theme-2);
}

/*滚动条里面轨道*/
::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
  background: var(--theme-1);
}
</style>
