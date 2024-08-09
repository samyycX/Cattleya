import axios from "axios"
import { useToast } from "primevue/usetoast"
import { ref } from "vue"

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

const mediaQuery = window.matchMedia('(min-width: 768px)')
export const isMobile = ref(!mediaQuery.matches);
const isMobileListener = (mediaQuery) => {
    isMobile.value = !mediaQuery.matches; 
}

mediaQuery.addEventListener("change", isMobileListener);
