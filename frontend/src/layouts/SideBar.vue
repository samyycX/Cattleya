<template>
  <div class="flex flex-col bg-theme-0 py-2 pb-24 lg:py-20">
    <div class="flex flex-col mx-auto w-8/12 gap-3">
      <img src="@/assets/img/logo.png" class="aspect-square rounded-xl"/> 
      <div class="flex flex-row justify-around">
        <img src="@/assets/img/icon/github.svg" class="size-6 cursor-pointer" @click="toGithub"/>
        <img src="@/assets/img/icon/discord.svg" class="size-6 cursor-pointer" @click="toDiscord"/>
        <EnvelopeIcon class="size-6 cursor-pointer text-theme-5" @click="toEmail" />
      </div>
      <div class="flex flex-row gap-2 text-left">
        <UserCircleIcon class="size-6 text-theme-5" />
        <p class="text-theme-5">samyyc</p>
      </div>
      <MyTimezoneClock />
      <div class="flex flex-row gap-2 text-left">
        <HeartIcon class="size-6 text-theme-5" /> 
        <p class="text-theme-5">已存活 {{ survivedDays }} 天</p>
      </div>
      <div class="flex flex-row gap-2 text-left">
        <MapPinIcon class="size-6 text-theme-5" /> 
        <p class="text-theme-5">China, Shanghai</p>
      </div>
      <HeartRate />
    </div>
    <NavigatorEntries class="w-8/12 mx-auto mt-28"/>
    <div class="mt-auto">
      <p class="text-theme-5">2024 samyyc.dev</p>
    </div>
  </div>
</template>

<script setup>
import { EnvelopeIcon } from '@heroicons/vue/24/solid';
import { HeartIcon, MapPinIcon, UserCircleIcon } from '@heroicons/vue/24/outline';
import { computed } from 'vue';
import HeartRate from '@/components/general/HeartRate.vue';
import MyTimezoneClock from '@/components/general/MyTimezoneClock.vue';
import NavigatorEntries from '@/components/layout/NavigatorEntries.vue';

const survivedDays = computed(() => parseInt((new Date() - new Date("2008-05-08 16:30:00")) / (1000*60*60*24)))

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


