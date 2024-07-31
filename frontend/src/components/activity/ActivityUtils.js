export function formatActivityDate(date) {
  var nowDate = new Date()
  if (nowDate - date < 1 * 60 * 1000) {
    return "刚刚"
  } else if (nowDate - date < 60 * 60 * 1000) {
    return `${parseInt((nowDate - date) / 60000 )}分钟前`
  } else if (nowDate - date < 24 * 60 * 60 * 1000) {
    return `${parseInt((nowDate - date) / 3600000 )}小时前`
  }
  return `${date.getFullYear()}年${date.getMonth()+1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`
}