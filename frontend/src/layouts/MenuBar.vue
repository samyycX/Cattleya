<template>
    <div id="menubar" aria-orientation="horizontal">
        <Toast></Toast>
        <MenuBar :model="items">
            <template #item="{ item, props }">
                <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
                    <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                        <span :class="item.icon"></span>
                        <span class="ml-2">{{  item.label }}</span>
                    </a>
                </router-link>
            </template>
            <template #end>
                <div class="flex items-center gap-2">
                    <Avatar :image="avatar" v-if="avatar != null" shape="circle"></Avatar>
                    <Button :label="user.username" v-if="user != null" class="text-color-secondary" @click="userPopoverToggle" text></Button>
                    <Button label="登入" v-if="user == null" icon="pi pi-sign-in" class="text-color-secondary" @click="gotoUserLogin" text></Button>
                    <Popover ref="popover">
                        <div class="flex flex-column w-10rem">
                            <Button label="用户设置" class="text-color-secondary" icon="pi pi-spin pi-cog" text @click="gotoUserSetting"></Button>
                            <Button label="登出" class="text-color-secondary" icon="pi pi-sign-out" text @click="userLogout"></Button>
                        </div>
                    </Popover>
                </div>
            </template>
        </MenuBar>
    </div>
</template>

<script setup>
import axios from 'axios';
import Avatar from 'primevue/avatar';
import MenuBar from 'primevue/menubar';
import Popover from 'primevue/popover';
import Button from 'primevue/button';
import { useRouter } from 'vue-router';
import { ref } from 'vue'
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import { useUserLogStateStore } from '@/stores/userlogstate';
const router = useRouter()
const toast = useToast()
const userLogState = useUserLogStateStore()
const items = ref([
    {
        "label": "Home",
        "route": "/",
        "icon": 'pi pi-home'
    },
    {
        "label": "Hello",
        "route": "/hello"
    }
])

const user = ref(null)
const avatar = ref(null)

//component variable

const popover = ref()

const refreshUser = () => {
    axios.get("/api/user/info").then((resp) => {
        const result = resp.data;
        if (result.code == 200) {
            user.value = result.data
            axios.get("/api/user/avatar").then((resp) => {
                const result = resp.data;
                if (result.code == 200) {
                    avatar.value = result.data;
                }
            })
        } else {
            user.value = null
            avatar.value = null
        }
    }).catch(() => {
        user.value = null
        avatar.value = null
    })
}

userLogState.$subscribe(() => {
    refreshUser()
})

const userPopoverToggle = (event) => {
    popover.value.toggle(event);
}

const gotoUserSetting = () => {
    router.push({ name: 'usercenter' })
}

const gotoUserLogin = () => {
    router.push({ name: 'login' })    
}

const userLogout = () => {
    axios.post("/api/user/logout").then((resp) => {
        const result = resp.data;
        if (result.code == 200) {
            toast.add({ severity: "success", "summary": "拜拜~", detail: "ε≡ﾍ( ´∀`)ﾉ", life: 3000 })
            router.push({ name: 'login' })
        }
    })
    userLogState.logout()
}

refreshUser()
</script>