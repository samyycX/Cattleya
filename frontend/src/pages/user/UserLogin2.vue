<template>
  <div class="mx-auto">
    <div class="flex flex-row w-[48rem] h-[32rem] border-solid border-4 m-auto login-box border-theme-4 relative">
      <div class="flex flex-col w-1/12 border-r-4 border-theme-4 border-right">
        <button class="bg-theme-4 h-1/2 tracking-widest text-3xl [writing-mode:vertical-lr] switch-login text-theme-1" @click="onLoginSwitch">登录
        </button>
        <button
          class="h-1/2 tracking-widest text-3xl [writing-mode:vertical-lr] switch-register text-theme-4" @click="onRegisterSwitch">注册</button>
      </div>
      <div id="input-box" class="flex flex-col gap-2 my-3 mx-auto justify-center w-72">
        <div class="flex flex-row h-fit shrink text-2xl justify-center">
          <UserIcon class="size-9 inline text-theme-4"></UserIcon>
          <div class="flex flex-col w-full ml-1"> 
            <input type="text"
              class="outline-none border-solid border border-theme-4 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
              placeholder="账户名"
              v-model="user.username" />
            <p class="text-sm text-red-700 text-left" v-if="warnings.username != ''">{{ warnings.username }}</p> 
          </div>
        </div>
        <div class="flex flex-row h-fit text-2xl justify-center">
          <KeyIcon class="size-9 inline text-theme-4"></KeyIcon>
          <input type="password"
            class="outline-none border-solid border border-theme-4 bg-theme-1 ml-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
            placeholder="密码"
            v-model="user.password"
            @focusout="checkPassword"
            />
          </div>
        <div class="flex flex-row h-fit text-2xl justify-center" v-if="isRegisterMode">
          <KeyIcon class="size-9 inline text-theme-4"></KeyIcon>
          <div class="flex flex-col w-full ml-1"> 
            <input type="password"
              class="outline-none border-solid border border-theme-4 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
              placeholder="请重复输入密码"
              v-model="user.repeatPassword"
              @focusout="checkRepeatPassword"
              />
            <p class="text-sm text-red-700 text-left" v-if="warnings.password != ''">{{ warnings.password }}</p>  
          </div>
        </div>
        <div class="flex flex-row h-fit text-2xl justify-center" v-if="isRegisterMode">
          <EnvelopeIcon class="size-9 inline text-theme-4"></EnvelopeIcon>
          <div class="flex flex-col w-full ml-1">
            <input type="email"
              class="outline-none border-solid border border-theme-4 bg-theme-1 px-1 placeholder:text-theme-4 w-full text-theme-5"
              placeholder="邮箱（选填）"
              v-model="user.email"
              @focusout="checkEmail"
              />
            <p class="text-sm text-red-700 text-left" v-if="warnings.email != ''">{{ warnings.email }}</p>  
          </div>
        </div>
        <div class="flex flex-row h-fit text-2xl justify-center" v-if="isRegisterMode">
          <PhoneIcon class="size-9 inline text-theme-4"></PhoneIcon>
          <div class="flex flex-col w-full ml-1">
            <input type="tel"
              class="outline-none border-solid border border-theme-4 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
              placeholder="手机号（选填）" 
              v-model="user.phone"
              @focusout="checkPhone"
              />
            <p class="text-sm text-red-700 text-left" v-if="warnings.phone != ''">{{ warnings.phone }}</p>
          </div>
        </div>
       <div class="flex flex-row h-fit mt-3 text-2xl">
          <button type="submit" class="outline-none bg-theme-4 text-theme-1 w-full h-full" @click="submit">{{ isRegisterMode ? "注册" : "登录" }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useNotification } from '@/stores/notifications';
import { useUserStore } from '@/stores/users';
import { UserIcon } from '@heroicons/vue/24/solid';
import { KeyIcon } from '@heroicons/vue/24/solid';
import { EnvelopeIcon } from '@heroicons/vue/24/solid';
import { PhoneIcon } from '@heroicons/vue/24/solid';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import * as utils from '@/utils/user' ;
// eslint-disable-next-line
const notificationStore = useNotification();
const router = useRouter();

const isRegisterMode = ref(false);

const warnings = ref({
  username: "",
  password: "",
  email: "",
  phone: ""
});

const userStore = useUserStore();
const user = ref({
    "username": null,
    "password": null,
    // 这个值只是给输入框做判断用，上传到后端的时候没有作用
    "repeatPassword": null,
    "email": "",
    "phone": ""
})

// 左侧按钮切换的两个函数
const onLoginSwitch = () => {
  isRegisterMode.value = false;

  var switchLogin = document.querySelector(".switch-login");
  var switchRegister = document.querySelector(".switch-register");
  switchLogin.style.backgroundColor = "var(--theme-4)";
  switchLogin.style.color = "var(--theme-1)";
  switchRegister.style.backgroundColor = "var(--theme-1)";
  switchRegister.style.color = "var(--theme-4)";
};

const onRegisterSwitch = () => {
  isRegisterMode.value = true;

  var switchLogin = document.querySelector(".switch-login");
  var switchRegister = document.querySelector(".switch-register");
  switchLogin.style.backgroundColor = "var(--theme-1)";
  switchLogin.style.color = "var(--theme-4)";
  switchRegister.style.backgroundColor = "var(--theme-4)";
  switchRegister.style.color = "var(--theme-1)";
}

const checkEmail = () => {
  warnings.value.email = utils.checkEmail(user.value.email) ? "" :  "邮箱格式错误 (´-ι_-｀)";
}

const checkPhone = () => {
  warnings.value.phone = utils.checkPhone(user.value.phone) ? "" : "手机号格式错误 (ㆆᴗㆆ)";
}

// 给第一个密码框使用，因为我们不希望只输入第一个密码框的时候就提示两次密码不对，所以这里只做消除警告的判断
const checkPassword = () => {
  if (user.value.password == user.value.repeatPassword) {
    warnings.value.password = ""
  }
}

const checkRepeatPassword = () => {
  if (user.value.password != user.value.repeatPassword) {
    warnings.value.password = "两次输入的密码不匹配 -`д´-"
  } else {
    warnings.value.password = ""
  }
}

const submit = () => {
    for (var warning in warnings.value) { 
      if (warnings.value[warning] != "") {
        notificationStore.add("error", warnings.value[warning]);
        return;
      }
    }
    
    if (!isRegisterMode.value) {
        axios.post("/api/auth/login", user.value).then(resp => {
            const result = resp.data;
            if (result.code != 200) {
                notificationStore.error(result.msg)
            } else {
                notificationStore.success("登录成功，正在跳转回上一页~");
                localStorage.TOKEN = result.token;
                userStore.setCurrentUser(result.id)
                setTimeout(router.back, 2000);
            }
        })
    } else {
        axios.post("/api/users/", user.value).then((resp) => {
            const result = resp.data;
            if (result.code != 200) {
              notificationStore.error(result.msg);
            } else {
                notificationStore.success("注册成功，正在跳转回上一页~");
                localStorage.TOKEN = result.token;
                userStore.setCurrentUser(result.id)
                setTimeout(router.back, 2000);
            }
        });
    }
}
</script>

<style scoped>

#input-box {
  overflow-y: hidden;
  animation-timing-function: ease-in-out;
}

</style>
