<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.css" integrity="sha384-NFTC4wvyQKLwuJ8Ez9AvPNBv8zcC2XaQzXSMvtORKw28BdJbB2QE8Ka+OyrIHcQJ" crossorigin="anonymous">
  <div class="flex h-screen text-center bg-theme-1">
    <!--<MenuBar class="flex flex-column"></MenuBar>!-->
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <MainPage></MainPage> -->
    <NotificationOverlay />
    <router-view class="body flex flex-column"></router-view>
  </div>
</template>

<script setup>
import '@/assets/text/text.css'
import 'lxgw-wenkai-webfont/style.css'
import NotificationOverlay from './components/NotificationOverlay.vue';
</script>

<style>

:root {
  font-family: "Cascadia Mono Regular", "Source Han Sans", sans-serif;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
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
