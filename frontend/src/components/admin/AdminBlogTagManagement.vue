<template>
  <div class="overflow-x-visible flex flex-col text-theme-5 gap-5">
    <div class="flex flex-row gap-2">
      <input type="checkbox" class="outline-none" v-model="checkAll"/>
      <p>{{ selectedTags.size != 0 ? `已选中 ${selectedTags.size}/${tags.length} 项` : `共 ${tags.length} 项` }}</p>
      <div class="flex flex-row gap-2" v-if="selectedTags.size != 0">
        <p class="text-red-800 hover:underline hover:text-red-700 underline-offset-4 cursor-pointer" @click="switchConfirmDeleteSelected">删除</p>
      </div>
    </div>
    <div class="flex flex-col gap-8 text-theme-5 h-max overflow-x-visible md:mr-16">
      <div v-for="tag in tags" :key="tag.id" class="flex flex-row gap-5 h-max text-xs md:text-md">
        <div class="flex flex-col justify-center">
          <input type="checkbox" class="outline-none" @click="() =>switchSelectedTag(tag)" :checked="selectedTags.has(tag.id)"/>
        </div>
        <div class="flex flex-col text-left">
          <p class="text-theme-5 text-lg">{{ tag.name }}</p>
          <p class="text-theme-5/75">共 {{ tag.count }} 篇博客</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useNotification } from '@/stores/notifications';
import { usePopup } from '@/stores/popups';
import { useProgress } from '@/stores/progresses';
import axios from 'axios';
import { onBeforeMount, reactive, ref, watch } from 'vue';


const tags = ref([])
const notification = useNotification()
const progress = useProgress()
const popup = usePopup()

const checkAll = ref(false);

const selectedTags = reactive(new Set())

watch(checkAll, () => {
	if (checkAll.value) {
		tags.value.forEach(t => selectedTags.add(t.id))
	} else {
		selectedTags.clear()
	}
})
const getTags = () => {
  axios.get("/api/blog-tags/").then((resp) => {
    const result = resp.data;
    if (result.code != 200) {
      notification.error(result.msg);
    } else {
      tags.value = result.data;
    }
  });
}
onBeforeMount(() => {
  getTags()
})
const switchSelectedTag = (tag) => {
	if (!selectedTags.has(tag.id)) {
		selectedTags.add(tag.id)
	} else {
		selectedTags.delete(tag.id)
	}
}
const getTagNameFromId = (tagId) => {
  return tags.value.find(tag => tag.id === tagId).name
}
const refresh = () => {
	selectedTags.clear()
  tags.value = []
  getTags()
}
const switchConfirmDeleteSelected = (blog) => {
  popup.addPopup("confirm", {
    title: `确定要删除选中的 ${selectedTags.size} 条标签吗?`,
    type: "dangerous",
    confirm: () => deleteSelected()
  })
}

const deleteSelected = () => {
	let tasks = []
	selectedTags.forEach(tag => { tasks.push({ title: `删除: ${getTagNameFromId(tag)}` }) })
	progress.addTasks(refresh, ...tasks)
	Array.from(selectedTags).forEach( (tag, index) => {
		axios.delete(`/api/blog-tags/${tag}/`).then(resp => {
			if (resp.status == 204) {
				progress.updateProgress(index, 'success')
			} else {
				progress.updateProgress(index, 'fail')
				progress.updateMsg(index, resp.data.msg)
			}
		})
	})
}
</script>