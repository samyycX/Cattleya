import axios from "axios";
import { defineStore } from "pinia";

export const useUserStore = defineStore('users', {
    state: () => {
        return { users: [] }
    },
    actions: {
        adduser(user) {
            this.users.push(user)
        },
        async getuser(id) {
            var user = this.users.find((user) => user.id == id )
            if (user != undefined) {
                return Promise.resolve(user)
            }
            var promise = axios.get("/api/user/info", { params: { id } }).then(async (resp) => {
                const result = resp.data;
                if (result.code == 200) {
                    var user = result.data;
                    return await axios.get("/api/user/avatar", { params: { id } }).then((resp) => {
                        const result = resp.data;
                        if (result.code == 200) {
                            user.avatar = result.data;
                            if (this.users.findIndex((user) => user.id == id ) == -1 ){
                                this.users.push(user)
                            }
                            return user
                        }
                    })
                }
            })
            return promise
        }
    }
})