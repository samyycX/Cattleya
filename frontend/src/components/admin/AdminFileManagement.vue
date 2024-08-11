<template>
	<div class="h-full w-full flex flex-col">
		<div class="fixed h-screen w-screen left-0 top-0 flex flex-col justify-center backdrop-blur-md text-theme-5" v-if="detailFile != null">
			<div class="flex flex-col w-11/12 lg:w-1/2 h-5/6 m-auto p-4 bg-theme-0 border-2 border-theme-5 gap-3 text-left overflow-scroll">
				<div class="w-full cursor-pointer max-h-[50%]">
					<img :src="detailFile.path" v-if="isImage(detailFile)" class="w-auto h-auto max-w-full max-h-full m-auto" />
					<div v-else class="w-full aspect-square flex flex-col justify-center">
						<DocumentIcon class="size-12 m-auto text-theme-5" />
					</div>
				</div>
				<table class="list-disc ml-0 md:ml-4 text-xs md:text-lg">
					<tr>
						<th>ID</th>
						<th>{{ detailFile.id }}</th>
					</tr>
					<tr>
						<th>文件名</th>
						<th>{{ detailFile.name }}</th>
					</tr>
					<tr>
						<th>HASH</th>
						<th>{{ detailFile.hash }}</th>
					</tr>
					<tr>
						<th>创建日期</th>
						<th>{{ new Date(detailFile.created_time) }}</th>
					</tr>
					<tr>
						<th>创建者</th>
						<th> {{ detailFile.created_by.nickname }}</th>
					</tr>
				</table>
				<div class="mt-auto mb-4 flex flex-row w-full justify-end px-4">
					<button class="outline-none leading-none p-2 bg-theme-5 text-theme-0 rounded-md hover:text-theme-1/75" @click="detailFile = null">确认</button>
				</div>
			</div>
		</div>
		<div class="flex flex-row gap-4 text-theme-5">
			<input type="checkbox" class="bg-theme-0 outline-none cursor-pointer" :checked="currentPageSelectedAll" @click="checkAllCurrentPage"/>
			<p>{{selectedFiles.length == 0 ? `共 ${filesCount} 项` : `已选中 ${selectedFiles.length}/${filesCount} 项`}}</p>
			<div v-if="selectedFiles.length != 0" class="text-sm flex flex-row justify-center">
				<p class="text-red-800 underline underline-offset-4 hover:text-red-600 cursor-pointer" @click="deleteSelected">删除</p>
			</div>
		</div>
		<div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-10 gap-3">
			<div v-for="file in displayingFiles" :key="file.id" class="p-2 hover:border-theme-4 border-transparent border-2 rounded-sm " 
				:style="file.selected ? `border-color: rgb(var(--theme-4))` : `border-color: transparent`"
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
							<input type="checkbox" class="bg-theme-0 outline-none cursor-pointer leading-none m-auto" :checked="file.selected" @click="() => switchSelectedFile(file)"/>
						</div>
						<div class="flex flex-col min-w-0 min-h-0">
							<p class="text-theme-5/70 text-xs underline underline-offset-2 hover:text-theme-5 cursor-pointer" @click="detailFile = file">查看详情</p>
							<p class="text-theme-5 truncate text-xs"	@click="() => { if (isMobile) { switchSelectedFile(file) } }">{{  file.name  }}</p>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="flex flex-row gap-2 text-theme-5 justify-end w-full pt-3 pr-12" v-show="detailFile == null ">
			<Paginator ref="paginator" v-model="paginatorData" />
		</div>
	</div>
</template>

<script setup>
import { DocumentIcon } from '@heroicons/vue/24/solid';
import axios from 'axios';
import { watch, reactive, ref, watchEffect, computed } from 'vue';
import Paginator from '../general/Paginator.vue';
import { isMobile } from '@/utils';
import { useProgress } from '@/stores/progresses';

const progress = useProgress();

const filesCount = ref()
const files = reactive(new Map());

const paginator = ref();

const paginatorData = ref({
	start: 0,
	limit: 30,
	count: filesCount.value
})

const displayingFiles = ref(new Set())
const currentPageSelectedAll = computed(() => !Array.from(displayingFiles.value).map(f => f.selected == true).includes(false));
const selectedFiles = computed(() => files.size != 0 ? Array.from(files.values()).map((a) => Array.from(a)).flat().filter(file => file.selected == true ) : [])

const detailFile = ref(null)

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

const switchSelectedFile = (file) => {
	file.selected = !file.selected
}

const isImage = (file) => {
	for (var ext of [".png", ".jpg", ".jpeg", ".avif", ".gif", ".webp"]) {
		if (file.path.toLowerCase().endsWith(ext)) {
			return true;
		}
	}
	return false;
}

const checkAllCurrentPage = () => {
  if (currentPageSelectedAll.value) {
		displayingFiles.value.forEach(f => f.selected = false)
	} else {
		displayingFiles.value.forEach(f => f.selected = true)
	}
}

const refresh = () => {
	displayingFiles.value.clear()
	files.clear();
	paginator.value.to(0)
	requestFiles(0, true)
}

const deleteSelected = () => {
	let tasks = []
	selectedFiles.value.forEach(file => { tasks.push({ title: `删除: ${file.id}` }) })
	progress.addTasks(refresh, ...tasks)
	selectedFiles.value.forEach( (file, index) => {
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

<style scoped>
::-webkit-scrollbar {
	display: none;
}
</style>