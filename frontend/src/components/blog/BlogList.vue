<template>
  <div>
    <div class="flex flex-col gap-8 text-theme-5 h-max overflow-x-visible">
      <div v-for="blog in blogs" :key="blog.id" class="flex flex-row gap-5 h-max">
        <div class="flex flex-col gap-2 justify-between grow">
          <div class="w-full flex flex-row justify-between">
            <p class="text-2xl cursor-pointer underline md:no-underline hover:underline underline-offset-4 text-theme-8" @click="() => toBlog(blog.id)">{{ blog.title }}</p>
            <p class="text-sm text-theme-5/80 my-auto" hidden>#{{ blog.id }}</p>
            <p class="leading-none my-auto">{{ new Date(blog.created_time).toDateString() }}</p>
          </div>
          <div class="w-full flex flex-row gap-2 text-center text-theme-5/80 text-sm">
            <ArrowPathIcon class="size-3 my-auto" />
            <p class="leading-none">{{ getLastUpdatedInterval(blog.updated_time) }} AGO</p>
          </div>
          <div class="w-full flex flex-row text-theme-5/80">
            <p>{{ blog.author.nickname }}</p>
            <p class="ml-5">共 {{ blog.length }} 字</p>
            <p class="text-sm text-theme-5/80 my-auto leading-none ml-5" hidden>#{{ blog.id }}</p>
            <div class="ml-auto flex flex-row gap-2">
              <div v-for="tag in blog.tags" :key="tag.id" class="flex flex-row text-sm">
                <p class="underline underline-offset-4 cursor-pointer hover:text-theme-5">#{{ tag.name }}</p>
              </div>
            </div>
            <div class="ml-auto" v-if="blog.tags.length == 0">
              <p class="text-theme-5/80 text-sm">此文章暂无标签</p>
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-between py-2" v-if="props.isAdmin">
          <div class="">
            <ArchiveBoxXMarkIcon class="size-6 text-red-800 cursor-pointer" @click="() => switchConfirmDeleteBlog(blog)" />
          </div>
          <EyeIcon class="size-6 text-theme-5 cursor-pointer" v-if="!blog.visible" @click="() => switchPublish(blog)"/>
          <EyeSlashIcon class="size-6 text-theme-5 cursor-pointer" v-else @click="() => switchPublish(blog)"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useNotification } from '@/stores/notifications';
import { ArrowPathIcon } from '@heroicons/vue/24/outline';
import { ArchiveBoxXMarkIcon, EyeIcon,EyeSlashIcon } from '@heroicons/vue/24/outline';
import axios from 'axios';
import { defineProps, reactive, defineModel } from 'vue';
import { useRouter } from 'vue-router';
import { usePopup } from '@/stores/popups';

const blogs = defineModel()
const props = defineProps(["isAdmin"])
const router = useRouter();
const notification = useNotification();
const popup = usePopup();

const getLastUpdatedInterval = (time) => {

  var interval = new Date() - new Date(time);
  if (interval < 1000 * 60 * 60) {
    return `${parseInt(interval/(1000*60))}MIN`
  } else if (interval < 1000 * 60 * 60 * 24) {
    return `${parseInt(interval/(1000*60*60))}HOUR`
  } else {
    return `${parseInt(interval/(1000*60*60*24))}DAY`
  }
};

const toBlog = (id) => {
  router.push({ path: `/blog/${id}` });
}

const switchConfirmDeleteBlog = (blog) => {
  popup.addPopup("confirm", {
    title: "确定要删除吗?",
    type: "dangerous",
    confirm: () => deleteBlog(blog.id)
  })
}

const deleteBlog = (id) => {
  axios.delete(`/api/blogs/${id}/?visible=all`).then(resp => {
    const result = resp.data;
    if (resp.status == 204) {
      notification.success("删除成功")
      blogs.value.splice(blogs.value.find(blog => blog.id == id), 1)
    } else {
      notification.error(result.msg)
    }
  });
}

const switchPublish = async (blog) => {
  axios.patch(`/api/blogs/${blog.id}/?visible=all`, {
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
