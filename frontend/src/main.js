import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import Aura from '@primevue/themes/aura'

import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'

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
    name: 'test', path: '/test', component: () => import("./pages/activity/ActivityPage.vue")
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      prefix: '',
      darkModeSelector: 'system'
    }
  }
})
app.use(pinia)
app.use(ConfirmationService);
app.use(ToastService);
app.use(router)
app.mount('#app')
