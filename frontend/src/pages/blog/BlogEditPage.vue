<template>
  <div class="h-full w-full flex flex-row bg-theme-0 text-left text-xl relative overflow-hidden">
    <FileInput hidden ref="fileInput" :allow-multiple="true" :notify="true" @success="onUploadSuccess" @fail="() => {}"/>
    <div class="flex-1 border-theme-5 p-2">
      <div class="flex flex-col gap-3 h-full">
        <div class="flex flex-row gap-3 w-full" >
          <button class="flex-1 border-theme-4 border-2 bg-theme-0" @click="save">保存</button>
          <button class="flex-1 bg-theme-4 text-theme-0" @click="switchPublish">{{ blog.visible ? "取消发布" : "发布" }}</button>
        </div>
        <input type="text" class="border-theme-4 border-2 outline-none bg-theme-0 pl-2" v-model="blog.title" placeholder="请输入标题.." />
        <BlogTagSelection ref="tagSelection"/>
        <textarea ref="contentInput" id="content-input" class="outline-none h-full w-full resize-none bg-theme-0" placeholder="在此处输入..." v-model="blog.content" @drop="onDrop"/>
      </div>
    </div>
    <div class="absolute h-[98%] left-1/2 top-1/2 -translate-y-1/2 -translate-x-1/2 w-[2px] bg-theme-5 my-auto"></div>
    <div id="preview" class="flex-1 flex text-xl text-wrap prose prose-cattleya p-2 max-w-none overflow-x-hidden overflow-y-scroll" @scrollend="onPreviewScrollEnd">
      <BlogMdxRender id="render" class="text-wrap w-full break-words" :content="renderContent" />
    </div>
  </div>
</template>

<script setup>
import BlogTagSelection from '@/components/blog/tag/BlogTagSelection.vue';
import BlogMdxRender from '@/components/blog/BlogMdxRender.vue';
import { computed, ref, watch, reactive } from 'vue';
import FileInput from '@/components/file/FileInput.vue';
import { onMounted } from 'vue';
import { useNotification } from '@/stores/notifications';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/users';

const notification = useNotification();
const route = useRoute();
const userStore = useUserStore();
const user = ref({});

const blog = reactive({
  title: "",
  content: "",
  visible: false
})

const renderContent = computed(() => `# ${blog.title}\n${blog.content}`)

const lastScrollTo = ref(0);
const lastScrollToEnd = ref(false);


const imageExts = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"]

const fileInput = ref()
const contentInput = ref()
const tagSelection = ref()

const isManuallyScrolled = ref(false)

const currentBlogId = ref(null)

watch(blog, () => {
  var elem = document.getElementById("preview");
  setTimeout(() => elem.scrollTop = elem.scrollHeight, 100);
})

const onDrop = (e) => {
  e.preventDefault();
  fileInput.value.upload(e.dataTransfer.files);
}

onMounted(async () => {
  var elem = document.getElementById("preview");
  "mousedown wheel DOMMouseScroll mousewheel keyup touchmove".split(" ").map(e => elem.addEventListener(e, () => {
    isManuallyScrolled.value = true;
  }));
  user.value = await userStore.getCurrentUser();
  axios.get(`/api/blogs/${route.params.blogId}/`).then((resp) => {
    const result = resp.data;
    if (result.code == 200) {
      if (result.data.author != user.value.id) {
        notification.error("你无权修改这篇博客")
      } else {
        Object.assign(blog, result.data)
      }
    } else {
      notification.error(result.msg)
    }
  })
});


const onPreviewScrollEnd = (e) => {

  if (isManuallyScrolled.value) {
    lastScrollTo.value = e.target.scrollTop;
    lastScrollToEnd.value = e.target.scrollTop + e.target.clientHeight == e.target.scrollHeight
    isManuallyScrolled.value = false;
    return;
  }
  if (lastScrollToEnd.value) {
    lastScrollTo.value = e.target.scrollHeight;
  }
  e.target.scrollTop = lastScrollTo.value;
}

const onUploadSuccess = (data) => {
  for (var file of data) {
    const index = document.activeElement.id == "content-input" ? contentInput.value.selectionStart : blog.content.length;
    if (imageExts.map(ext => file.path.endsWith(ext)).includes(true)) {
      blog.content = "\n" + blog.content.slice(0, index) + `![](${file.path})` + blog.content.slice(index) + "\n"
    } else {
      blog.content = "\n" + blog.content.slice(0, index) + `[${file.path}](${file.path})` + blog.content.slice(index) + "\n"
    }
  } 
}

const save = async () => {
  var resp;
  if (currentBlogId.value == null) {
    if (blog.title == "") {
      notification.error("请先输入标题")
      return false;
    }
    resp = await axios.post("/api/blogs/", {
      ...blog,
      tags: tagSelection.value.selectedTags.map(tag => tag.id)
    })
  } else {
    resp = await axios.patch(`/api/blogs/${currentBlogId.value}/`, {
      ...blog,
      tags: tagSelection.value.selectedTags.map(tag => tag.id)
  })

  }
  const result = resp.data;
  if (result.code == 200) {
    notification.success("保存成功")
    if (currentBlogId.value == null) {
      currentBlogId.value = result.data.id;
    }
    return true;
  } else {
    notification.error(result.msg)
    return false;
  }
}

const switchPublish = async () => {
  if (!await save()) {
    return
  }
  console.log(!blog.visible);
  axios.patch(`/api/blogs/${currentBlogId.value}/`, {
    visible: !blog.visible
  }).then((resp) => {
    const result = resp.data;
    if (result.code == 200) {
      notification.success(!blog.visible ? "发布成功!" : "取消发布成功！")
      blog.visible = !blog.visible
    } else {
      notification.error(result.msg)
    }
  })
}

</script>

<style scoped>

</style>
