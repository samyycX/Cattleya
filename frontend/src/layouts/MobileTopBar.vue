<template>
  <div>
    <div class="flex flex-col gap-3 mt-5 border-b-2 border-theme-5 pb-2 m-3">
      <div class="flex flex-row gap-3">
        <img src="@/assets/img/logo.png" class="aspect-square rounded-xl size-16"/> 
        <div class="flex flex-col gap-2 my-auto">
          <div class="flex flex-row justify-around">
            <img src="@/assets/img/icon/github.svg" class="size-6 cursor-pointer" @click="toGithub"/>
            <img src="@/assets/img/icon/discord.svg" class="size-6 cursor-pointer" @click="toDiscord"/>
            <EnvelopeIcon class="size-6 cursor-pointer text-theme-5" @click="toEmail" />
          </div>
          <div class="flex flex-row gap-2 text-left">
            <UserCircleIcon class="size-6 text-theme-5" />
            <p class="text-theme-5">samyyc</p>
          </div>
        </div>
        <div class="size-10 my-auto ml-auto text-theme-5" @click="expanded = !expanded">
          <Bars3Icon v-if="!expanded" />
          <XMarkIcon v-else/>
        </div>
      </div>
      <div class="flex flex-row justify-between">
        <MyTimezoneClock />
        <HeartRate class="my-auto" />
      </div>
      <div v-if="expanded">
        <NavigatorEntries />
      </div>
    </div>
  </div>
</template>

<script setup>
import { EnvelopeIcon, Bars3Icon, XMarkIcon } from '@heroicons/vue/24/solid';
import { UserCircleIcon } from '@heroicons/vue/24/outline';
import { ref } from 'vue';
import HeartRate from '@/components/general/HeartRate.vue';
import MyTimezoneClock from '@/components/general/MyTimezoneClock.vue';
import NavigatorEntries from '@/components/layout/NavigatorEntries.vue';

const expanded = ref(false)

const toGithub = () => {
  window.open("https://github.com/samyycX")
}
const toDiscord = () => {
  window.open("https://discordapp.com/users/1046322446464192583")
}
const toEmail = () => {
  window.open("mailto:3356207189@qq.com")
}
</script>
