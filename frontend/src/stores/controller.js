import { defineStore } from "pinia";

export const useController = defineStore("controller",{
  state: () => {
    return {
      menu: true
    }
  },
  actions: {
    showMenu() {
      this.menu = true;
    },
    hideMenu() {
      this.menu = false;
    }
  }
})
