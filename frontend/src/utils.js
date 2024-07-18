
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