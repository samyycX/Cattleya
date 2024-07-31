import axios from "axios"
import { useToast } from "primevue/usetoast"

export function formatDate(date) {
    var year = date.getFullYear()
    var month = date.getMonth() + 1
    var day = date.getDate()
    var hour = date.getHours().toString().padStart(2, "0")
    var minute = date.getMinutes().toString().padStart(2, "0")
    var second = date.getSeconds().toString().padStart(2, "0")
    var millisecond = date.getMilliseconds().toString().padStart(3, "0")
    return `${year}年${month}月${day}日 ${hour}时${minute}分${second}.${millisecond}秒`
}

export function toastError(toast, msg) {
    msg.forEach(m => toast.add({ severity: 'error', summary: m, life: 3000 }))
}

export function toastSuccess(toast, msg) {
    toast.add({ severity: 'success', summary: msg[0], life: 3000 })
}

// export async function getCurrentUser() {
//     return new Promise((await axios.get(`/api/user/${localStorage.USER_ID}/`)).data)
// }