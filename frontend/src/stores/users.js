import axios from "axios";
import { defineStore } from "pinia";

export const useUserStore = defineStore('user', {
    state: () => {
        return { currentUser: null, users: new Map() }
    },
    actions: {
        adduser(user) {
            this.users.set(user.id, user)
        },
        logged() {
            return this.currentUser == null
        },
        async setCurrentUser(id) {
            this.currentUser = await this.getuser(id)
        },
        clearCurrentUser() {
            this.currentUser = null;
        },
        async getCurrentUser() {
            if (this.currentUser == null && localStorage.TOKEN) {
                const id = (await axios.get(`/api/users/whoami/`)).data.data
                await this.setCurrentUser(id)
            }
            return this.currentUser
        },
        async getuser(id) {
            if (this.users.has(id)) {
                return Promise.resolve(this.users.get(id))
            }
            var promise = axios.get(`/api/users/${id}/`).then(resp => {
                this.adduser(resp.data)
                return resp.data
            })
            return promise
        }
    }
})