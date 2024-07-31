<template>
  <div>
    <!--<MenuBar class="flex flex-column"></MenuBar>!-->
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <MainPage></MainPage> -->
    <router-view class="body flex flex-column"></router-view>
  </div>
</template>

<script setup>
import '@/assets/text/text.css'
import MenuBar from './layouts/MenuBar.vue';
</script>

<style>
:root {
  --font-family: "PingFang SC", -apple-system, 'Helvetica Neue', Helvetica, 'Nimbus Sans L', Arial, 'Liberation Sans', 'Hiragino Sans GB',
    'Source Han Sans CN', 'Source Han Sans SC', 'Microsoft YaHei', 'Wenquanyi Micro Hei', 'WenQuanYi Zen Hei', 'ST Heiti', SimHei,
    'WenQuanYi Zen Hei Sharp', sans-serif !important;

}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

.body {
  padding-top: 20px;
}
</style>
