<template>
  <div class="overflow-x-visible flex flex-col text-theme-5 gap-5">
    <div class="flex flex-row gap-2">
      <input type="checkbox" class="outline-none" :checked="currentPageSelectedAll" @click="checkAllCurrentPage"/>
      <p>{{ selectedBlogs.length ? `已选中 ${selectedBlogs.length}/${blogsCount} 项` : `共 ${blogsCount} 项` }}</p>
      <p class="text-theme-5/70 hover:underline hover:text-theme-5 underline-offset-4 cursor-pointer" @click="router.push({ name: 'blog-new' })">新建</p>
      <div class="flex flex-row gap-2" v-if="selectedBlogs.length != 0">
        <p class="text-red-800 hover:underline hover:text-red-700 underline-offset-4 cursor-pointer" @click="switchConfirmDeleteSelected">删除</p>
        <p class="text-theme-5/70 hover:underline hover:text-theme-5 underline-offset-4 cursor-pointer" @click="publishSelected">发布全部</p>
        <p class="text-theme-5/70 hover:underline hover:text-theme-5 underline-offset-4 cursor-pointer" @click="hideSelected">隐藏全部</p>
      </div>
    </div>
    <div class="flex flex-col gap-8 text-theme-5 h-max overflow-x-visible md:mr-16">
      <div v-for="blog in displayedBlogs" :key="blog.id" class="flex flex-row gap-5 h-max text-xs md:text-md">
        <div class="flex flex-col justify-center">
          <input type="checkbox" class="outline-none" @click="() =>switchSelectedBlog(blog)" :checked="blog.selected"/>
        </div>
        <div class="flex flex-col gap-0 justify-between grow">
          <div class="w-full flex flex-row justify-between">
            <p class="text-2xl cursor-pointer underline md:no-underline hover:underline underline-offset-4 text-theme-8" @click="() => toBlog(blog.id)">{{ blog.title }}</p>
            <p class="leading-none my-auto text-sm md:text-lg">{{ new Date(blog.created_time).toDateString() }}</p>
          </div>
          <div class="w-full flex flex-row gap-2 text-center text-theme-5/80">
            <ArrowPathIcon class="size-3 my-auto" />
            <p class="leading-none text-xs md:text-sm">{{ getLastUpdatedInterval(blog.updated_time) }} AGO</p>
          </div>
          <div class="w-full flex flex-row text-theme-5/80 text-sm md:text-md">
            <p>{{ blog.author.nickname }}</p>
            <p class="ml-5">共 {{ blog.length }} 字</p>
            <p class="text-sm text-theme-5/80 my-auto leading-none ml-5" hidden>#{{ blog.id }}</p>
            <div class="ml-auto flex flex-row gap-2">
              <div v-for="tag in blog.tags" :key="tag.id" class="flex flex-row text-xs md:text-md">
                <p class="underline underline-offset-4 cursor-pointer hover:text-theme-5" @click="() => toBlogTag(tag)">#{{ tag.name }}</p>
              </div>
            </div>
            <div class="ml-auto" v-if="blog.tags.length == 0">
              <p class="text-theme-5/80">此文章暂无标签</p>
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-between py-2">
          <div class="">
            <ArchiveBoxXMarkIcon class="size-6 text-red-800 cursor-pointer" @click="() => switchConfirmDeleteBlog(blog)" />
          </div>
          <EyeIcon class="size-6 text-theme-5 cursor-pointer" v-if="!blog.visible" @click="() => switchPublish(blog)"/>
          <EyeSlashIcon class="size-6 text-theme-5 cursor-pointer" v-else @click="() => switchPublish(blog)"/>
        </div>
      </div>
    </div>
    <div class="flex flex-row gap-2 text-theme-5 justify-end w-full pt-3 pr-12">
			<Paginator ref="paginator" v-model="paginatorData" />
		</div>
  </div>
</template>

<script setup>
import { useNotification } from '@/stores/notifications';
import { usePopup } from '@/stores/popups';
import { useProgress } from '@/stores/progresses';
import { ArchiveBoxXMarkIcon, ArrowPathIcon, EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline';
import axios from 'axios';
import { watchEffect, watch, reactive, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import Paginator from '../general/Paginator.vue';

const router = useRouter();
const notification = useNotification()
const popup = usePopup()
const progress = useProgress()

const paginator = ref()

const blogsCount = ref();
const blogs = reactive(new Map());
const displayedBlogs = ref(new Set())
const currentPageSelectedAll = computed(() => !Array.from(displayedBlogs.value).map(f => f.selected == true).includes(false));
const selectedBlogs = computed(() => blogs.size != 0 ? Array.from(blogs.values()).map((a) => Array.from(a)).flat().filter(blog => blog.selected == true ) : [])


const paginatorData = ref({
	start: 0,
	limit: 10,
	count: blogsCount.value
})

const requestBlogs = (start, display) => {
	axios.get(`/api/blogs/?visible=all`, { params: { limit: paginatorData.value.limit, offset: start } }).then(resp => {
		paginatorData.value.count = blogsCount.value = resp.data.data.count;
		blogs.set(start, new Set(resp.data.data.results))
		if (display) {
			displayedBlogs.value = blogs.get(start)
		}
	})
}

watchEffect(() => {
	if (blogs.has(paginatorData.value.start)) {
		displayedBlogs.value = blogs.get(paginatorData.value.start)
	} else {
		requestBlogs(paginatorData.value.start, true)
	}
})

const switchSelectedBlog = (blog) => {
	blog.selected = !blog.selected
}

const checkAllCurrentPage = () => {
  if (currentPageSelectedAll.value) {
		displayedBlogs.value.forEach(f => f.selected = false)
	} else {
		displayedBlogs.value.forEach(f => f.selected = true)
	}
}

const refresh = () => {
  displayedBlogs.value.clear()
	blogs.clear();
	paginator.value.to(0)
	requestBlogs(0, true)
}

const getBlogTitleFromId = (blogId) => {
  console.log(blogs.values().next().value)
  for (var value of blogs.values().next().value) {
    if (value.id === blogId) {
      return value.title
    }
  }
}

const switchConfirmDeleteSelected = (blog) => {
  popup.addPopup("confirm", {
    title: `确定要删除选中的 ${selectedBlogs.value.length} 篇博客吗?`,
    type: "dangerous",
    confirm: () => deleteSelected()
  })
}

const deleteSelected = () => {
	let tasks = []
	selectedBlogs.value.forEach(blog => { tasks.push({ title: `删除: ${blog.title}` }) })
	progress.addTasks(refresh, ...tasks)
	selectedBlogs.value.forEach( (blog, index) => {
		axios.delete(`/api/blogs/${blog.id}/?visible=all`).then(resp => {
			if (resp.status == 204) {
				progress.updateProgress(index, 'success')
			} else {
				progress.updateProgress(index, 'fail')
				progress.updateMsg(index, resp.data.msg)
			}
		})
	})
}

const publishSelected = () => {
	let tasks = []
	selectedBlogs.value.forEach(blog => { tasks.push({ title: `发布: ${blog.title}` }) })
	progress.addTasks(refresh, ...tasks)
	selectedBlogs.value.forEach( (blog, index) => {
		axios.patch(`/api/blogs/${blog.id}/?visible=all`, { visible: true }).then(resp => {
			if (resp.data && resp.data.code == 200) {
				progress.updateProgress(index, 'success')
			} else {
				progress.updateProgress(index, 'fail')
				progress.updateMsg(index, resp.data.msg)
			}
		})
	})
}

const hideSelected = () => {
	let tasks = []
	selectedBlogs.value.forEach(blog => { tasks.push({ title: `隐藏: ${blog.title}` }) })
	progress.addTasks(refresh, ...tasks)
	selectedBlogs.value.forEach( (blog, index) => {
		axios.patch(`/api/blogs/${blog.id}/?visible=all`, { visible: false }).then(resp => {
			if (resp.data && resp.data.code == 200) {
				progress.updateProgress(index, 'success')
			} else {
				progress.updateProgress(index, 'fail')
				progress.updateMsg(index, resp.data.msg)
			}
		})
	})
}

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
router.push({ path: `/blog/edit/${id}` });
}
const toBlogTag = (tag) => {
  window.location.href = `/blog/list?tag=${tag.id}`;
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
