import { defineStore } from "pinia";

export const useUserLogStateStore = defineStore('userlogstate', {
    state: () => {
        return { state: false }
    },
    actions: {
        login() {
            this.state = true
        },
        logout() {
            this.state = false
        }
    }
})