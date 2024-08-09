<template>
  <div class="flex flex-col notification absolute left-1/2 top-3 -translate-x-[16rem] w-[32rem] h-fit">
    <TransitionGroup name="notifications" tag="div">
      <div v-for="notification in notificationStore.notifications.values()" :key="notification.uid" :style="'background-color: ' + getColor(notification)" class="flex flex-row w-full bg-theme-2 pl-2 mb-2">
        <CheckIcon class="size-6 text-theme-1" v-if="notification.type == 'success' "/>
        <XMarkIcon class="size-6 text-theme-1" v-if="notification.type == 'error' " />
        <span class="msg text-xl text-theme-1 text-left text-theme-1">{{ notification.msg }}</span>
      </div>
    </TransitionGroup> 
  </div>
</template>

<script setup>
import { TransitionGroup } from 'vue';
import { useNotification } from '@/stores/notifications';
import { CheckIcon } from '@heroicons/vue/24/solid';
import { XMarkIcon } from '@heroicons/vue/24/solid';
const notificationStore = useNotification();

const getColor = (notification) => {
  if (notification.type == "success") {
    return 'var(--success)'
  } else if (notification.type == "error") {
    return 'var(--error)'
  }
  return 'var(--theme-5)'
}

</script>

<style scoped>
.notifications-move,
.notifications-enter-active,
.notifications-leave-active {
  transition: all 0.5s ease;
}
.notifications-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}
.notifications-leave-to {
  opacity: 0;
  transform: translateX(30px);
} 
</style>
