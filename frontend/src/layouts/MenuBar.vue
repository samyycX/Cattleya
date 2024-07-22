<template>
    <div id="menubar" aria-orientation="horizontal">
    <Toast></Toast>
    <ConfirmPopup></ConfirmPopup>
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
                    <Avatar :image="userStore.currentUser.avatar" v-if="userStore.currentUser != null" shape="circle"></Avatar>
                    <Button :label="userStore.currentUser.nickname" v-if="userStore.currentUser != null" class="text-color-secondary" @click="userPopoverToggle" text></Button>
                    <Button label="登入" v-if="userStore.currentUser == null" icon="pi pi-sign-in" class="text-color-secondary" @click="gotoUserLogin" text></Button>
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
import Toast from 'primevue/toast';
import ConfirmPopup from 'primevue/confirmpopup';
import { useRouter } from 'vue-router';
import { computed, ref } from 'vue'
import { useToast } from 'primevue/usetoast';
import { useUserStore } from '@/stores/users';
const router = useRouter()
const toast = useToast()
const userStore = useUserStore()
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

//component variable

const popover = ref()

const user = userStore.currentUser
if (localStorage.TOKEN) {
    axios.get("/api/users/whoami/").then(resp => userStore.setCurrentUser(resp.data.data))
}



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
    axios.get("/api/auth/logout").then((resp) => {
        const result = resp.data;
        if (result.code == 200) {
            localStorage.removeItem("TOKEN")
            userStore.clearCurrentUser()
            toast.add({ severity: "success", "summary": "拜拜~", detail: "ε≡ﾍ( ´∀`)ﾉ", life: 3000 })
            router.push({ name: 'login' })
        }
    }),
    userStore.clearCurrentUser()
}
</script>