<template>
  <div>
    <div ref="dom" class="flex flex-row gap-2 border-b-[1.5px] border-transparent hover:border-theme-5 underline-offset-4 cursor-pointer w-fit" @mouseenter="showUnderline" @mouseleave="onMouseLeave" @click="jumpTo">
      <p class="text-theme-5/70 leading-none my-auto text-sm">{{ index }}</p>
      <p class="text-theme-6 cursor-pointer text-lg leading-6">{{ props.entry.title }}</p>
    </div>
    <div v-for="child in props.entry.children" :key="child.id" class="ml-5">
      <BlogDirectoryEntry :entry="child" />
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue';
import { watchEffect, defineProps, computed, ref } from 'vue';
const props = defineProps(['entry']);
const dom = ref();

const scrollTo = inject('scroll-to')

const index = computed(() => {
  if (!("level" in props.entry)) {
    return "";
  }

  var levels = []
  var lastLevel = 0

  for (var level of props.entry.level) {
    if (level != lastLevel) {
      levels.push(1)
      lastLevel = level;
    } else {
      levels[levels.length - 1] += 1
    }
  }
  return levels.join(".")
})

const jumpTo = () => {
  if (props.entry.top != undefined) {
    document.getElementById("blog-scrollable-container").scrollTop = props.entry.top
  }
  scrollTo(props.entry);
}

const showUnderline = () => {
  if (dom.value == null) {
    return;
  }
  dom.value.style.borderColor = "rgb(var(--theme-5))"
}

const hideUnderline = () => {
  if (dom.value == null) {
    return;
  }
  dom.value.style.borderColor = "transparent"
}

const onMouseLeave = () => {
  if (!props.entry.activate) {
    hideUnderline();
  }
}

watchEffect(() => {
  if (dom.value == null) {
    return;
  }
  if (props.entry.activate) {
    showUnderline();
  } else {
    hideUnderline();
  }
})


</script>
