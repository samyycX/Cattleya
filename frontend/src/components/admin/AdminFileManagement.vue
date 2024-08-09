<template>
	<div class="h-full w-full flex flex-col">
		<div class="flex flex-row gap-4 text-theme-5">
			<input type="checkbox" class="bg-theme-0 outline-none cursor-pointer" v-model="checkAll"/>
			<p>{{selectedFiles.size == 0 ? `共 ${filesCount} 条数据` : `选中 ${selectedFiles.size}/${filesCount} 条数据`}}</p>
			<div v-if="selectedFiles.size != 0" class="text-sm flex flex-row justify-center">
				<p class="text-red-800 underline underline-offset-4 hover:text-red-600 cursor-pointer" @click="deleteSelected">删除</p>
			</div>
		</div>
		<div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-10 gap-3">
			<div v-for="file in displayingFiles" :key="file.id" class="p-2 hover:border-theme-4 border-transparent border-2 rounded-sm " 
				:style="selectedFiles.has(file.id) ? `border-color: rgb(var(--theme-4))` : `border-color: transparent`"
				>
				<div class="flex flex-col gap-1 text-left">
					<div class="aspect-square w-full cursor-pointer hidden md:inline" @click="() => switchSelectedFile(file)">
						<img :src="file.path" v-if="isImage(file)" class="aspect-square w-full object-cover" />
						<div v-else class="w-full aspect-square flex flex-col justify-center">
							<DocumentIcon class="size-12 m-auto text-theme-5" />
						</div>
					</div>
					<div class="flex flex-row w-full inline gap-2">
						<div class="inline md:hidden">
							<input type="checkbox" class="bg-theme-0 outline-none cursor-pointer leading-none m-auto" :checked="selectedFiles.has(file.id)" @click="() => switchSelectedFile(file)"/>
						</div>
						<div class="flex flex-col min-w-0 min-h-0">
							<p class="text-theme-5/70 text-xs underline underline-offset-2 hover:text-theme-5 cursor-pointer">查看详情</p>
							<p class="text-theme-5 truncate text-xs"	@click="() => { if (isMobile) { switchSelectedFile(file) } }">{{  file.name  }}</p>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="flex flex-row gap-2 text-theme-5 justify-end w-full pt-3 pr-12">
			<Paginator ref="paginator" v-model="paginatorData" />
		</div>
	</div>
</template>

<script setup>
import { DocumentIcon } from '@heroicons/vue/24/solid';
import axios from 'axios';
import { watch, reactive, ref, watchEffect } from 'vue';
import Paginator from '../general/Paginator.vue';
import { isMobile } from '@/utils';
import { useProgress } from '@/stores/progresses';

const progress = useProgress();

const filesCount = ref()
const files = new Map();

const paginator = ref();

const paginatorData = ref({
	start: 0,
	limit: 30,
	count: filesCount.value
})

const displayingFiles = ref(new Set())

const requestFiles = (start, display) => {
	axios.get(`/api/files/`, { params: { limit: paginatorData.value.limit, offset: start } }).then(resp => {
		paginatorData.value.count = filesCount.value = resp.data.data.count;
		files.set(start, new Set(resp.data.data.results))
		if (display) {
			displayingFiles.value = files.get(start)
		}
	})
}

watchEffect(() => {
	if (files.has(paginatorData.value.start)) {
		displayingFiles.value = files.get(paginatorData.value.start)
	} else {
		requestFiles(paginatorData.value.start, true)
	}
})

const selectedFiles = reactive(new Set())

const switchSelectedFile = (file) => {
	if (!selectedFiles.has(file.id)) {
		selectedFiles.add(file.id)
	} else {
		selectedFiles.delete(file.id)
	}
}

const checkAll = ref(false);

watch(checkAll, () => {
	if (checkAll.value) {
		displayingFiles.value.forEach(f => selectedFiles.add(f.id))
	} else {
		selectedFiles.clear()
	}
})

const isImage = (file) => {
	for (var ext of [".png", ".jpg", ".jpeg", ".avif", ".gif", ".webp"]) {
		if (file.path.toLowerCase().endsWith(ext)) {
			return true;
		}
	}
	return false;
}

const refresh = () => {
	displayingFiles.value.clear()
	selectedFiles.clear()
	files.clear();
	paginator.value.to(0)
	requestFiles(0, true)
}
const deleteSelected = () => {
	let tasks = []
	selectedFiles.forEach(file => { tasks.push({ title: `删除: ${file}` }) })
	progress.addProgresses(refresh, ...tasks)
	Array.from(selectedFiles).forEach( (file, index) => {
		axios.delete(`/api/files/${file}/`).then(resp => {
			if (resp.data && resp.data.code == 200) {
				progress.updateProgress(index, 'success')
			} else {
				progress.updateProgress(index, 'fail')
			}
		})
	})
}

</script>
