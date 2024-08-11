import { defineStore } from "pinia";
import { reactive } from "vue";

export const useProgress = defineStore('progress', {
    state: () => {
        return {
            onAllDone: null,
            tasks: []
        }
    },
    actions: {
        addTasks(onAllDone, ...tasks) {
            if (this.tasks.length != 0) {
                return
            }
            this.onAllDone = () => {
                if (onAllDone) onAllDone();
                this.tasks.splice(0, this.tasks.length)
                this.onAllDone = null;
            }
            tasks.map((task, index) => { task.progress = 0; task.index = index; })
            this.tasks.push(...tasks)
        },
        updateProgress(index, progress) {
            this.tasks[index].progress = progress;
        },
        updateMsg(index, msg) {
            this.tasks[index].msg = msg;
        }
    }
});