<template>

    <ConfirmPopup></ConfirmPopup>

    <div id="info">
        <div class="avatar-container">
            <img id="avatar" :src="avatar" />
            <div id="avatar-overlay" @click="callRealAvatarInputDom">
                <i class="pi pi-upload"></i>
            </div>
            <input type="file" id="avatarfile" @change="uploadAvatar" hidden/>
            <Dialog :header="avatarWarning" v-model:visible="avatarWarningVisible" modal>
                <template #footer>
                    <Button label="OK" @click="avatarWarningVisible = false" />
                </template>
            </Dialog>
        </div>
        <p class="text-color" id="username">{{ user.username }}</p>
        <div class="flex flex-column gap-2">
            
            <div class="flex flex-row gap-4 info-block">
                <p class="text-color">密码</p>
                <Button class="info-right" @click="passwordChangeDialogVisible = true">点我修改</Button>
                <Dialog v-model:visible="passwordChangeDialogVisible" modal header="修改密码">
                    <div class="flex flex-row gap-4 info-block">
                        <p class="text-color">旧密码</p>
                        <InputText type="password" v-model="passwordChangeValues.oldPassword" class="info-right" autocomplete="off" />
                    </div>
                    <div class="flex flex-row gap-4 info-block">
                        <p class="text-color">新密码</p>
                        <InputText type="password" v-model="passwordChangeValues.newPassword" class="info-right" autocomplete="off" @input="monitorPasswordChange"/>
                    </div>
                    <div class="flex flex-row gap-4 info-block">
                        <p class="text-color">再次输入新密码</p>
                        <InputText type="password" v-model="passwordChangeValues.repeatNewPassword" class="info-right" autocomplete="off" @input="monitorPasswordChange"/>
                    </div>
                    <p class="text-red-500">{{ passwordChangeWarning }}</p>
                    <div class="flex justify-content-end gap-2">
                        <Button type="button" label="取消" severity="secondary" @click="passwordChangeDialogVisible = false"></Button>
                        <Button type="button" label="保存" @click="changePassword"></Button>
                    </div>
                </Dialog>
                <Dialog header="修改成功！" v-model:visible="passwordChangeSuccessDialogVisible" modal>
                    <template #footer>
                        <Button label="OK" @click="passwordChangeSuccessDialogVisible = false" />
                    </template>
                </Dialog>
            </div>
            <div class="flex flex-row gap-4 info-block">    
                <p class="text-color">邮箱</p>
                <InputText type="text" class="info-right" v-model="user.email" placeholder="请输入你的邮箱" />
            </div>
            <div class="flex flex-row gap-4 info-block">
                <p class="text-color">手机号</p>
                <InputText type="text" class="info-right" v-model="user.phone" placeholder="请输入你的手机号"/>
            </div>
            <div class="flex flex-row gap-4 info-block">
                <p class="text-color">注册时间</p>
                <p class="info-right text-color">{{ formatDate(new Date(user.registered_time)) }}</p>
            </div>
            <div class="flex flex-row flex-grow-1 gap-2 control">
                <Button id="cancel" class="flex-1" severity="secondary" @click="confirmReset($event)">重置！</Button>
                <Button id="submit" class="flex-1" @click="confirmSubmit($event)">提交修改！</Button>
            </div>
        </div>
    </div>
    
</template>

<script setup>
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import ConfirmPopup from 'primevue/confirmpopup';
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import axios from 'axios';
import { ref } from 'vue';
import { formatDate } from '@/utils'
import { useRouter } from 'vue-router';
var user = ref({})
var initialUser = Object.assign({}, user.value)

var avatar = ref("")

// component variable
const confirm = useConfirm();
const toast = useToast();
const router = useRouter();

var passwordChangeDialogVisible = ref(false)
var passwordChangeWarning = ref("")
var passwordChangeValues = ref({
    oldPassword: '',
    newPassword: '',
    repeatNewPassword: ''
})
var passwordChangeSuccessDialogVisible = ref(false)

var avatarWarningVisible = ref(false)
var avatarWarning = ref("不支持此文件")


const refreshUser = () => {
    axios.get("/api/user/info").then((resp) => {
        const result = resp.data;
        if (result.code == 200) {
            user.value = result.data;
            initialUser = Object.assign({}, user.value)
        } else {
            router.push({ name: "login" })
        }
    }).catch(() => {
        router.push({ name: "login" })
    })
}

const refreshAvatar = () => {
    axios.get("/api/user/avatar").then((resp) => {
        var result = resp.data;
        if (result.code == 200) {
            avatar.value = result.data;
        }
    })
}

const resetInfo = () => {
    console.log(initialUser)
    user.value = Object.assign({}, initialUser);
}

const monitorPasswordChange = () => {
    if (passwordChangeValues.value.newPassword != passwordChangeValues.value.repeatNewPassword) {
        passwordChangeWarning.value = "两次输入密码不匹配"
    } else {
        passwordChangeWarning.value = ""
    }
}

const changePassword = () => {
    if (passwordChangeValues.value.newPassword != passwordChangeValues.value.repeatNewPassword) {
        passwordChangeWarning.value = "两次输入密码不匹配"
        return
    }
    axios.post(
        "/api/user/changepassword",
        {
            "oldPassword": passwordChangeValues.value.oldPassword,
            "newPassword": passwordChangeValues.value.newPassword
        }
    ).then((resp) => {
        const result = resp.data;
        if (result.code != 200) {
            passwordChangeWarning.value = result.msg
        } else {
            passwordChangeDialogVisible.value = false
            passwordChangeSuccessDialogVisible.value = true
        }
    })
}

const callRealAvatarInputDom = () => {
    document.getElementById("avatarfile").click()
}

const uploadAvatar = ({ target }) => {
    var file = target.files[0]
    var splited = file.name.split(".")
    if (splited.length < 2 || !["jpg", "png", "jpeg", "bmp"].includes(splited[splited.length-1].toLocaleLowerCase())) {
        avatarWarning.value = "不支持此文件"
        avatarWarningVisible.value = true
        return
    }
    const formData = new FormData();
    formData.append("file", file)
    axios.post("/api/user/avatar", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    .then(resp => {
        var result = resp.data;
        if (result.code != 200) {
            avatarWarning.value = result.msg;
        } else {
            refreshAvatar()
        }
    })
    .catch(error => {
        alert(error)
    })
}

const submit = () => {
    axios.post("/api/user/info", user.value).then((resp) => {
        const result = resp.data;
        if (result.code == 200) {
            toast.add({ severity: "success", summary: "修改成功！", life: 3000 })
            initialUser = Object.assign({}, user.value)
        } else {
            toast.add({ severity: 'error', summary: "修改错误...", detail: result.msg, life: 3000 })
        }
    })
}

const confirmSubmit = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: "确定要提交吗？",
        icon: 'pi pi-exclamation-circle',
        rejectLabel: "取消",
        rejectIcon: 'pi pi-times',
        reject: () => {},
        acceptLabel: "确定！",
        acceptIcon: 'pi pi-check',
        accept: submit
    })
}

const confirmReset = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: "确定要重置吗？",
        icon: 'pi pi-exclamation-circle',
        rejectLabel: "取消",
        rejectIcon: 'pi pi-times',
        reject: () => {},
        acceptLabel: "确定！",
        acceptIcon: 'pi pi-check',
        accept: resetInfo
    })
}
refreshUser()
refreshAvatar()

</script>

<style scoped>
#info {
    width: 400px;
    margin: auto;
}
.avatar-container {
    width: 320px;
    height: 320px;
    margin: auto;
}
#avatar {   
    width: 320px;
    height: 320px;
    border-radius: 1000px;
    margin: 0;
}
#avatar-overlay {
    margin: 0;
    position: absolute;
    width: 320px;
    height: 320px;
    transform: translateY(-324px);
    opacity: 0;
    transition: .5s ease;
    background-color: rgba(122, 122, 122, 0.5);
    border-radius: 1000px;
}
#avatar-overlay > i {
    margin-top: 50%;
    scale: 5;
}
.avatar-container:hover #avatar-overlay {
    opacity: 1;
}

#username {
    font-size: 30px;
}
.info-block > p {
    padding: 0;
}
.info-right {
    height: 80%;
    margin: auto 0 auto auto;
    justify-content: center
}
button.info-right {
    width: 200px;
}
.control > button {
    justify-content: center;
}
</style>