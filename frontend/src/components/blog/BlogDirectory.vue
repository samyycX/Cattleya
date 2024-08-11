<template>
  <div class="text-left">
    <div class="flex flex-row gap-2 mb-2">
      <HashtagIcon class="size-7 text-theme-5 my-auto" />
      <p class="text-2xl text-theme-5 text-left">目录</p>
    </div>
    <BlogDirectoryEntry :entry="entry" class="-translate-x-5"/>
  </div>
</template>

<script setup>
import { computed, defineProps, defineExpose, onMounted, ref, reactive, provide } from 'vue';
import { HashtagIcon } from '@heroicons/vue/24/outline';
import BlogDirectoryEntry from './BlogDirectoryEntry.vue';
const props = defineProps(["content", "title"])
const entries = ref([])
const entry = computed(() => {return { title:"", children: entries.value }})
const activated = ref({})

let jumping = false

const getTail = (node) => {
  if (node.children.length != 0) {
    return getTail(node.children.at(-1));
  }
  return node;
}

const parseMarkdownToTree = (markdown) => {

  const lines = Array.prototype.concat(`# ${props.title}`, markdown.split('\n'));
  const root = { children: [] };
  let stack = [root];
  var id = 1;
  lines.forEach(line => {
    const match = line.match(/^(#{1,6})\s+(.*)$/);
    if (match) {
      const level = match[1].length; // #的数量表示标题的级别
      const title = match[2].trim();

      // 创建新的节点
      const newNode = { id, title, children: [] };
      id++;

      // 找到父节点
      while (stack.length > level) {
        stack.pop();
      }

      // 添加新节点到父节点的children
      const father = stack[stack.length - 1]
      newNode.level = [...Array(father.children.length+1).keys()].map(() => level);
      if (father.level != undefined) {
        newNode.level = Array.prototype.concat(father.level, newNode.level)
      }
      newNode.prev = getTail(father);
      newNode.prev.next = newNode;
      father.children.push(newNode);
      stack.push(newNode);
    }
  });
  root.children[0].prev = null;
  return root.children;
}

onMounted(() => {
  entries.value = parseMarkdownToTree(props.content);
})

const bindDoms = (entry, contentContainer) => {
  var level = Object.assign([], entry.level)
  for (var child of contentContainer) {
    if (child.tagName == `H${level[0]}`) {
      level.splice(0,1);
    }
    if (level.length == 0) {
      entry.top = child.offsetTop;
      // child.id = `entry-${entry.id}`
      break;
    }
  }
  for (var childEntry of entry.children) {
    bindDoms(childEntry, contentContainer)
  }
}

const startBindDoms = (contentContainer) => {
  for (var entry of entries.value) {
    bindDoms(entry, contentContainer)
  }
  activated.value = entries.value[0]
  activated.value.activate = true;
}

const deactivateAll = (nodes, id) => {
  for (var node of nodes) {
    if (node.id != id) {
      node.activate = false;
    }
    if (node.children.length != 0) {
      deactivateAll(node.children, id);
    }
  }
}

const scrollTo = (entry) => {
  jumping = true
  activated.value = entry;
  entry.activate = true;
  deactivateAll(entries.value, entry.id);
}

const onScroll = (scrollTop) => {
  if (jumping) {
    jumping = false;
    return;
  }
  if (scrollTop == 0) {
    activated.value.activate = false;
    activated.value = entries.value[0];
    activated.value.activate = true;
    return;
  }
  if (scrollTop < activated.value.top && activated.value.prev != null) {
    activated.value.activate = false;
    activated.value = activated.value.prev;
    activated.value.activate = true;
  } 
  if (activated.value.next != undefined && scrollTop > activated.value.next.top) {
    activated.value.activate = false;
    activated.value = activated.value.next;
    activated.value.activate = true;
  }
}

provide('scroll-to', scrollTo);

defineExpose({ startBindDoms, onScroll })

</script>
