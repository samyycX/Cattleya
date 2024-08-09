<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.css" integrity="sha384-NFTC4wvyQKLwuJ8Ez9AvPNBv8zcC2XaQzXSMvtORKw28BdJbB2QE8Ka+OyrIHcQJ" crossorigin="anonymous">
  <div id="body" class="flex flex-col sm:flex-row w-screen h-screen text-center bg-theme-0 overflow-y-scroll md:overflow-y-hidden">

    <NotificationOverlay class="z-[1000] " />
    <PopupOverlay class="z-[1001] " />
    <ProgressBarOverlay class="z-[999] " />
    <SideBar class="w-3/12 overflow-y-scroll lg:min-w-2/12 lg:overflow-hidden" v-if="(!isMobile) && menu"/>
    <MobileTopBar v-if="isMobile && menu" class="" />

    <div class="px-4 md:w-full md:px-0 pb-32 md:pb-0">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import '@/assets/text/text.css'
import NotificationOverlay from './components/NotificationOverlay.vue';
import SideBar from './layouts/SideBar.vue';
import MobileTopBar from './layouts/MobileTopBar.vue';
import { ref, watchEffect } from 'vue';
import { isMobile } from './utils';
import { useController } from './stores/controller';
import { storeToRefs } from 'pinia';
import PopupOverlay from './components/PopupOverlay.vue';
import ProgressBarOverlay from './components/ProgressBarOverlay.vue';

const controller = useController();
const { menu } = storeToRefs(controller);

</script>

<style>

:root {
  font-family: "Cascadia Mono Regular", "Source Han Sans", sans-serif;
}

body {
  overflow: hidden;
  width: 100%;
}

#app {
  -webkit-font-smoothing: antialiased;
  font-synthesis: none !important;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 0px;
}

::-webkit-scrollbar {
 /*高宽分别对应横竖滚动条的尺寸*/
  width: 10px;     
  height: 1px;
}

/*滚动条里面小方块*/
::-webkit-scrollbar-thumb {
 -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
  background: var(--theme-2);
}

/*滚动条里面轨道*/
::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
  background: var(--theme-1);
}
</style>
