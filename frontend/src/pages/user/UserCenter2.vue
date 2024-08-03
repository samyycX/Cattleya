<template>
  <div class="m-auto">
    <div class="flex flex-row w-[64rem] h-[32rem] border-solid border-4 border-theme-4">
      <div class="flex flex-col justify-center bg-theme-4 w-1/3">
        <transition name="avatar" mode="out-in">
          <div class="flex flex-col gap-4 w-full h-full justify-center" v-if="!isChangingPassword">
            <div id="avatar-container" class="mx-auto w-[160px] h-[160px] relative" @click="callAvatarUploadDom">
              <img :src="user.avatar" width="160px" height="160px" class="rounded-xl mx-auto"/>
              <div id="avatar-overlay" class="flex flex-col justify-center opacity-0 absolute w-[160px] h-[160px] left-0 top-0 backdrop-blur-sm rounded-xl" @click="callRealAvatarInputDom">
                  <ArrowUpTrayIcon class="text-theme-1 size-20 m-auto" />
              </div>
              <input type="file" id="avatar-upload-dom" @change="uploadAvatar" hidden />
            </div>
            <span class="text-theme-1 text-4xl">{{ user.username }}</span>
          </div>
          <div class="flex flex-col gap-4 w-full h-full justify-center" v-else-if="isChangingPassword">
            <div class="flex flex-col gap-3 w-3/4 mx-auto">
              <div class="flex flex-col text-xl"> 
                <input type="password"
                  class="outline-none border-solid border-2 border-theme-5 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
                  placeholder="旧密码"
                  v-model="passwords.oldPassword"
                />
                <p class="text-xs text-red-700 text-left" v-if="warnings.oldPassword != ''">{{ warnings.oldPassword }}</p> 
              </div>
              <div class="flex flex-col text-xl"> 
                <input type="password"
                  class="outline-none border-solid border-2 border-theme-5 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
                  placeholder="新密码"
                  v-model="passwords.newPassword"
                  @focusout="checkPassword"
                />
                <p class="text-xs text-red-700 text-left" v-if="warnings.nickname != ''">{{ warnings.nickname }}</p> 
              </div>
              <div class="flex flex-col text-xl"> 
                <input type="password"
                  class="outline-none border-solid border-2 border-theme-5 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
                  placeholder="重复输入新密码"
                  v-model="passwords.newRepeatPassword"
                  @focusout="checkRepeatPassword"
                />
                <p class="text-xs text-red-700 text-left" v-if="warnings.newRepeatPassword!= ''">{{ warnings.newRepeatPassword }}</p> 
              </div>
              <button type="submit" class="mt-3 w-full bg-theme-5 text-theme-1 text-xl" @click="changePassword">确认修改</button>
            </div>
          </div>
        </transition>
      </div>
      <div class="flex flex-col gap-2 my-3 mx-auto my-auto">
        <div class="flex flex-row h-fit shrink">
          <UserIcon class="size-9 inline text-theme-4"></UserIcon>
          <div class="flex flex-col w-full ml-1 text-xl justify-center"> 
            <input type="text"
              class="outline-none border-solid border-2 border-theme-4 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
              placeholder="昵称"
              v-model="user.nickname" />
            <p class="text-xs text-red-700 text-left" v-if="warnings.nickname != ''">{{ warnings.nickname }}</p> 
          </div>
        </div>
        <div class="flex flex-row h-full shrink">
          <KeyIcon class="size-9 inline text-theme-4 my-auto"></KeyIcon>
          <button class="bg-theme-4 text-theme-1 ml-1 w-full text-xl" @click="isChangingPassword = !isChangingPassword">{{ isChangingPassword ? "恢复" : "点我修改密码"}}</button> 
        </div>
        <div class="flex flex-row h-fit shrink">
          <EnvelopeIcon class="size-9 inline text-theme-4"></EnvelopeIcon>
          <div class="flex flex-col w-full ml-1 text-xl justify-center"> 
            <input type="text"
              class="outline-none border-solid border-2 border-theme-4 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
              placeholder="邮箱"
              v-model="user.email"
              @focusout="checkEmail"
            />
            <p class="text-xs text-red-700 text-left" v-if="warnings.email != ''">{{ warnings.email }}</p> 
          </div>
        </div>
        <div class="flex flex-row h-fit shrink">
          <PhoneIcon class="size-9 inline text-theme-4"></PhoneIcon>
          <div class="flex flex-col w-full ml-1 text-xl justify-center"> 
            <input type="text"
              class="outline-none border-solid border-2 border-theme-4 bg-theme-1 placeholder:text-theme-4 w-full px-1 text-theme-5"
              placeholder="手机号"
              v-model="user.phone" 
              @focusout="checkPhone"
            />
            <p class="text-xs text-red-700 text-left" v-if="warnings.phone != ''">{{ warnings.phone }}</p> 
          </div>
        </div>
        <button class="w-full bg-theme-1 text-theme-4 text-xl border-2 border-theme-4 mt-6" @click="resetInfo">放弃</button>
        <button class="w-full bg-theme-4 text-theme-1 text-xl" @click="submit">确认</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/users';
import { ref } from 'vue';
import axios from 'axios';
import { UserIcon, KeyIcon, ArrowUpTrayIcon, EnvelopeIcon, PhoneIcon } from '@heroicons/vue/24/solid';
import * as utils from '@/utils/user';
import { useNotification } from '@/stores/notifications';

const userStore = useUserStore();
const notification = useNotification();
const user = ref({})
var initialUser = {}

const refreshUser = () => {
    userStore.getCurrentUser().then(u => {user.value = u; initialUser = Object.assign({}, user.value)})
}

const isChangingPassword = ref(false);

refreshUser();

const warnings = ref({
  nickname: "",
  oldPassword: "",
  newRepeatPassword: "",
  email: "",
  phone: ""
});

const passwords = ref({
  oldPassword: "",
  newPassword: "",
  newRepeatPassword: ""
})


const resetInfo = () => {
    user.value = Object.assign({}, initialUser);
    for (var key in warnings.value) {
      warnings.value[key] = "";
    }
}
const checkEmail = () => {
  warnings.value.email = utils.checkEmail(user.value.email) ? "" :  "邮箱格式错误 (´-ι_-｀)";
}

const checkPhone = () => {
  warnings.value.phone = utils.checkPhone(user.value.phone) ? "" : "手机号格式错误 (ㆆᴗㆆ)";
}

// 给第一个密码框使用，因为我们不希望只输入第一个密码框的时候就提示两次密码不对，所以这里只做消除警告的判断
const checkPassword = () => {
  if (passwords.value.newPassword == passwords.value.newRepeatPassword) {
    warnings.value.newRepeatPassword = ""
  }
}

const checkRepeatPassword = () => {  
  if (user.value.password != user.value.repeatPassword) {
    warnings.value.newRepeatPassword = "两次输入的密码不匹配 -`д´-"
  } else {
    warnings.value.newRepeatPassword = ""
  }
}

const callAvatarUploadDom = () => {
  document.getElementById("avatar-upload-dom").click()
}

const changePassword = () => {
    if (warnings.value.newRepeatPassword != "") {
        return
    }
    axios.post(
        "/api/users/change_password/",
        {
            "old_password": passwords.value.oldPassword,
            "new_password": passwords.value.newPassword
        }
    ).then((resp) => {
        const result = resp.data;
        if (result.code != 200) {
            notification.error(result.msg)
        } else {
            notification.success(result.msg)
            isChangingPassword.value = false;
        }
    })
}

const uploadAvatar = ({ target }) => {
  var file = target.files[0];
  const formData = new FormData();
  formData.append("file", file)
  axios.post("/api/user-avatar", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  .then(resp => {
    var result = resp.data;
    if (result.code != 201) {
      notification.error(result.msg);
    } else {
      refreshUser()
      notification.success(result.msg);
    }
  })
  .catch(error => {
    alert(error)
  })
}

const submit = () => {
  axios.patch(`/api/users/${user.value.id}/`, user.value).then((resp) => {
    const result = resp.data;
    if (result.code) {
      notification.error(result.msg)
   } else {
      refreshUser();
      notification.success("修改成功！")
    }
  })
}

</script>

<style scoped>
.avatar-enter-active,
.avatar-leave-active {
  transition: opacity 0.3s ease;
}
.avatar-enter-from,
.avatar-leave-to {
  opacity: 0;
}

#avatar-container:hover #avatar-overlay {
  opacity: 1;
  transition: 0.4s ease;
}

#avatar-container:not(:hover) #avatar-overlay {
  opacity: 0;
  transition: 0.4s ease;
}
</style>
