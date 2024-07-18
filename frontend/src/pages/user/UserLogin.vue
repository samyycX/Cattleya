<template>
    <div class="container card flex gap-4 mb-4">
        <div>
            <SelectButton v-model="mode" :options="modes" aria-labelledby="basic"/>
        </div>
        <div>
            <InputText id="username" class="flex-auto w-full" placeholder="用户名" autocomplete="off" v-model="user.username"/>
        </div>
        <div>
            <Password id="password" class="password flex-auto w-full" input-class="w-full" :feedback="mode == '注册'" prompt-label="请输入密码" weak-label="太简单了！ /ᐠ｡ꞈ｡ᐟ\" medium-label="还可以~ ´-ω-)b" strong-label="不错！(╯✧∇✧)╯" placeholder="密码" autocomplete="off" v-model="user.password" @input="() => onPasswordChange(false)"/>
        </div>
        <div :hidden="mode == '登录'">
            <Password id="repeatPassword" class="password flex-auto w-full" input-class="w-full" :feedback="false" placeholder="请再次输入密码" autocomplete="off" v-model="user.repeatPassword" @input="() => onPasswordChange(true, false)"/>
        </div>
        <div :hidden="mode == '登录'">
            <InputText id="email" class="flex-auto w-full" placeholder="邮箱（选填）" autocomplete="off" v-model="user.email" @input="() => onEmailChange(false)"/>
        </div>
        <div :hidden="mode == '登录'">
            <InputText id="phone" class="flex-auto w-full" placeholder="手机号（选填）" autocomplete="off" v-model="user.phone" @input="() => onPhoneChange(false)"/>
        </div>
        <div :hidden="error == ''">
            <p id="warning" class="flex-auto w-full text-red-500">{{ error }}</p>
        </div>
        <div>
            <Button class="w-full justify-content-center" label="确认" @click="submit"></Button>
        </div>
    </div>
</template>

<script setup>

import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import SelectButton from 'primevue/selectbutton';
import Password from 'primevue/password';
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';
import { useUserLogStateStore } from '@/stores/userlogstate';
import axios from 'axios';

// eslint-disable-next-line
const EMAIL_REGEX = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
const PHONE_REGEX = /^1(3\d|4[5-9]|5[0-35-9]|6[2567]|7[0-8]|8\d|9[0-35-9])\d{8}$/

const toast = useToast();
const router = useRouter();
const userLogState = useUserLogStateStore()

// component variable
const mode = ref("登录")
const modes = ref(["登录","注册"])
const error = ref("")
const passwordMonitorActive = ref(false)

const user = ref({
    "username": null,
    "password": null,
    "repeatPassword": null,
    "email": "",
    "phone": ""
})

const onPasswordChange = (isRepeat, isGlobalCheck = false) => {
    if (isRepeat) {
        passwordMonitorActive.value = true
    }
    if (passwordMonitorActive.value) {
        if (user.value.password != user.value.repeatPassword) {
            error.value = "两次输入的密码不匹配 -`д´-"
        } else {
            if (!isGlobalCheck) {
                globalCheck()
            }   
        }
    }
}

const globalCheck = () => {
    if (mode.value == "登录") {
        return;
    }
    error.value = ""
    onEmailChange(true)
    onPasswordChange(false, true)
    onPhoneChange(true)
}

const onEmailChange = (isGlobalCheck = false) => {
    if (EMAIL_REGEX.exec(user.value.email) || user.value.email == "") {
        if (!isGlobalCheck) {
            globalCheck()
        }
    } else {
        error.value = "邮箱格式错误 (´-ι_-｀)"
    }
}

const onPhoneChange = (isGlobalCheck = false) => {
    if (PHONE_REGEX.exec(user.value.phone) || user.value.phone == "") {
        if (!isGlobalCheck) {
            globalCheck()
        }
    } else {
        error.value = "手机号格式错误 (ㆆᴗㆆ)"
    }
}

const submit = () => {
    globalCheck()
    if (error.value != "") {
        toast.add({ severity: "error", "summary": "(´ﾟдﾟ`)", "detail": error.value, "life": 5000 })
        return;
    }

    if (mode.value == "登录") {
        axios.post("/api/user/login", user.value).then((resp) => {
            const result = resp.data;
            if (result.code != 200) {
                error.value = result.msg;
                toast.add({ severity: "error", "summary": "(´ﾟдﾟ`)", "detail": error.value, "life": 5000 })
            } else {
                toast.add({ severity: "success", "summary": "(*‘ v`*)", "detail": "登录成功，正在跳转回上一页~", "life": 3000 })
                userLogState.login()
                setTimeout(router.back, 2000);
            }
        });
    } else {
        axios.post("/api/user/register", user.value).then((resp) => {
            const result = resp.data;
            if (result.code != 200) {
                error.value = result.msg;
                toast.add({ severity: "error", "summary": "(´ﾟдﾟ`)", "detail": error.value, "life": 5000 })
            } else {
                toast.add({ severity: "success", "summary": "(*‘ v`*)", "detail": "注册成功，正在跳转回上一页~", "life": 3000 })
                userLogState.login()
                setTimeout(router.back, 2000);
            }
        });
    }
}

</script>

<style scoped>
.container {
    max-width: 320px;
    margin: auto;
    margin-top: 10%;
}
#warning {
    text-align: left;
    margin: 0;  
}
</style>