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
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import axios from 'axios'

const app = createApp(App)
const pinia = createPinia()

const routes = [
  {
    name: 'mainpage', path: '/', component: () => import("./pages/MainPage.vue")
  },
  {
    name: 'usercenter', path: '/user/center', component: () => import("./pages/user/UserCenter.vue")
  },
  {
    name: 'login', path: '/user/login', component: () => import("./pages/user/UserLogin.vue")
  },
  {
    name: 'test', path: '/test', component: () => import("./pages/user/UserLogin2.vue")
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
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

// app.use(PrimeVue, {
//   theme: {
//     preset: Nora,
//     options: {
//       prefix: '',
//       darkModeSelector: 'system'
//     }
//   }
// })
//
//
//
app.use(pinia)
app.use(ConfirmationService);
app.use(ToastService);
app.use(router)
app.mount('#app')
