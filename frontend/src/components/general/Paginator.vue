<template>
	<div class="flex flex-row text-theme-5 gap-3 ">
		<button class="my-auto disabled:opacity-30" :disabled="page == 0">
			<ChevronDoubleLeftIcon class="my-auto size-4 hover:underline underline-offset-4 cursor-pointer" @click="to(0)"></ChevronDoubleLeftIcon>
		</button>
		<button class="my-auto disabled:opacity-30" :disabled="page == 0">
			<ChevronLeftIcon class="my-auto size-4 hover:underline underline-offset-4 cursor-pointer" @click="to(page-1)"></ChevronLeftIcon>
		</button>
		<p class="text-xs text-theme-5/70 hover:underline underline-offset-4 cursor-pointer leading-none my-auto" @click="to(page-2)">{{ page >= 2 ? page - 1 : "" }}</p>
		<p class="text-xs text-theme-5/70 hover:underline underline-offset-4 cursor-pointer leading-none my-auto" @click="to(page-1)">{{ page >= 1 ? page : "" }}</p>
		<div class="inline-block text-nowrap relative border-b-2 border-theme-5">
			<p class="inline-block h-full p-0 opacity-0 text-nowrap">{{ pageInput }}</p>
			<input type="number" class="text-md text-theme-5 bg-transparent outline-none text-center underline underline-offset-4 inline-block absolute left-0 top-0 p-0 h-full w-full" @focusout="pageInput = page + 1" @keydown="onKeydown" v-model="pageInput" />
		</div>
		<p class="text-xs text-theme-5/70 hover:underline underline-offset-4 cursor-pointer leading-none my-auto" @click="to(page+1)">{{ page <= pageMax - 2 ? page + 2 : "" }}</p>
		<p class="text-xs text-theme-5/70 hover:underline underline-offset-4 cursor-pointer leading-none my-auto" @click="to(page+2)">{{ page <= pageMax - 3 ? page + 3 : "" }}</p>
		<button class="my-auto disabled:opacity-30" :disabled="page == pageMax - 1">
			<ChevronRightIcon class="my-auto size-4 hover:underline underline-offset-4 cursor-pointer" @click="to(page+1)"></ChevronRightIcon>
		</button>
		<button class="my-auto disabled:opacity-30" :disabled="page == pageMax - 1">
			<ChevronDoubleRightIcon class="size-4 hover:underline underline-offset-4 cursor-pointer" @click="to(pageMax-1)"></ChevronDoubleRightIcon>
		</button>
	</div>
</template>

<script setup>
import { ChevronDoubleLeftIcon, ChevronDoubleRightIcon, ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/solid';
import { computed, defineModel, defineExpose, ref } from 'vue';

const data = defineModel()
const page = computed(() => Math.floor(data.value.start / data.value.limit))
const pageMax = computed(() => Math.ceil(data.value.count / data.value.limit));
const pageInput = ref(page.value + 1)

const to = (newPage) => {
	if (newPage >= pageMax.value || newPage < 0) {
		return;
	}
	data.value.start = newPage * data.value.limit
	pageInput.value = page.value + 1;
}

const onKeydown = (e) => {
	if (e.keyCode == 13) {
		to(parseInt(pageInput.value-1))
		e.preventDefault()
	}
}

defineExpose({ to })

</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}
</style>