import { defineStore } from "pinia";

const MAX_NOTIFICATION_AMOUNT = 5;

export const useNotification = defineStore('notification', {
  state: () => {
    return {
      notifications: new Map()
    }
  },
  actions: {
    append(notification) {
      if (this.notifications.size + 1 > MAX_NOTIFICATION_AMOUNT) {
        this.notifications.delete(this.notifications.keys().next())
      }
      var uid = new Date().valueOf();
      notification.uid = uid;
      this.notifications.set(uid, notification);
      setTimeout(() => {
        this.remove(uid);
      }, notification.time);
      return uid
    },
    add(type, msg, time = 2000) {
      if (Array.isArray(msg)) {
        for (var item of msg) {
          this.append({ msg: item, type, time });
        }
      } else {
        this.append({ msg, type, time });
      }
    },
    success(msg, time = 2000) {
      this.add("success", msg, time);
    },
    error(msg, time = 2000) {
      this.add("error", msg, time);
    },
    remove(uid) {
      this.notifications.delete(uid);
    },
    getAll() {
      return this.notifications.values()
    }
  },

})

