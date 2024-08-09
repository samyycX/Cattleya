import { defineStore } from "pinia";

export const usePopup = defineStore('popup', {
    state: () => {
        return {
            popups: []
        }
    },
    actions: {
        addPopup(type, params) {
            const uid = new Date().valueOf();
            params.cancel = () => this.removePopup(uid)
            this.popups.push({ uid, type, params })
        },
        removePopup(uid) {
            this.popups.splice(this.popups.find(popup => popup.uid == uid))
        }
    }
})