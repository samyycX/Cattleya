import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import Aura from '@primevue/themes/aura'
import Lara from '@primevue/themes/lara'
import Nora from '@primevue/themes/nora'
// import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import './assets/css/index.css'
import axios from 'axios'
import { useNotification } from './stores/notifications'
import { useUserStore } from './stores/users'
import { useController } from './stores/controller'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

const notification = useNotification()
const users = useUserStore()
const controller = useController()

const routes = [
  {
    name: 'mainpage', path: '/', component: () => import("./pages/MainPage.vue"), beforeEnter: (to, from, next) => {
      next('/blog/list')
    }
  },
  {
    name: 'usercenter', path: '/user/center', component: () => import("./pages/user/UserCenter2.vue")
  },
  {
    name: 'login', path: '/user/login', component: () => import("./pages/user/UserLogin2.vue")
  },
  {
    name: 'test', path: '/test', component: () => import("./pages/blog/BlogEditPage.vue")
  },
  {
    name: 'admin',
    path: '/admin',
    component: () => import("./pages/admin/AdminPage.vue"),
    beforeEnter: (to, from, next) => {
      axios.get(`/api/auth/isAdmin`).then((resp) => {
        if (resp.data.data) {
          next();
        } else {
          notification.error("你无权进入此页面")
          return false;
        }
      })
    }
  },
  {
    name: 'blog-edit',
    path: '/blog/edit/:blogId',
    component: () => import('./pages/blog/BlogEditPage.vue'),
    beforeEnter: (to, from, next) => {
      axios.get(`/api/blogs/${to.params.blogId}/?visible=all`).then(async (resp) => {
        const result = resp.data;
        if (result.code == 200) {
          const user = await users.getCurrentUser();
          if (result.data.author.id != user.id) {
            notification.error("你无权修改这篇博客")
            return false;
          } else {
            to.meta.blog = result.data;
            next();
          }
        } else {
          notification.error(result.msg)
          return false;
        }
      });

    }
  },
  {
    name: 'blog-new',
    path: '/blog/new/',
    component: () => import('./pages/blog/BlogEditPage.vue'),
  },
  {
    name: 'blog-list',
    path: '/blog/list',
    component: () => import('./pages/blog/BlogListPage.vue')
  },
  {
    name: 'blog',
    path: '/blog/:blogId',
    component: () => import("./pages/blog/BlogPage.vue"),
    beforeEnter: (to, from, next) => {
      axios.get(`/api/blogs/${to.params.blogId}/`).then((resp) => {
        const result = resp.data;
        if (result.code == 200) {
          to.meta.blog = resp.data.data;
          next();
        } else {
          notification.error(result.msg)
          return false;
        }
      });
    }
  },
  
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (["blog-edit", "blog-new", "admin"].includes(to.name)) {
    controller.hideMenu();
  } else {
    controller.showMenu();
  }
  users.getCurrentUser().then((user) => {
    to.meta.user = user;
    next()
  })
})

axios.interceptors.request.use(
  config => {
    if (localStorage.TOKEN) {
      config.headers.Authorization = `Token ${localStorage.TOKEN}`
    }
    return config
  },
  err => Promise.reject(err)
)

axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    console.log(error)
    if (error.response) {
      if (error.response.status == 401) {
        localStorage.TOKEN = undefined
        router.push({ name: "login" })
      }
    }
  }
)

app.use(PrimeVue, {
  theme: {
    preset: Nora,
    options: {
      prefix: '',
      darkModeSelector: 'system'
    }
  }
})

app.use(router)
app.mount('#app')
