<template>
  <div>
    <div class="flex flex-row gap-2 text-right md:text-left">
      <img src="@/assets/img/icon/heartbeat.svg" class="size-6" v-if="!isMobile" />
      <div class="flex flex-col ">
        <p class="text-red-800 leading-none">{{ heartrate }} BPM</p>
        <p class="text-theme-5 text-xs leading-none" v-if="heartrateLastUpdatedTime != null">({{ heartrateInterval }} AGO)</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, onUnmounted } from 'vue';
import axios from 'axios';
import { isMobile } from '@/utils';
const heartrate = ref("--")
const heartrateLastUpdatedTime = ref(null)
const heartrateInterval = computed(() => {
  if (heartrateLastUpdatedTime.value == null) return null;

  var interval = new Date() - heartrateLastUpdatedTime.value;
  if (interval < 1000 * 60 * 60) {
    return `${parseInt(interval/(1000*60))}MIN`
  } else if (interval < 1000 * 60 * 60 * 24) {
    return `${parseInt(interval/(1000*60*60))}HOUR`
  } else {
    return `${parseInt(interval/(1000*60*60*24))}DAY`
  }
})

var timerId;

onMounted(() => {
  timerId = setInterval( function getHealth() {
    axios.get("/api/health").then((resp) => {
      var data = resp.data.last_heartrate
      if (data != -1) {
        heartrate.value = parseInt(data);
        heartrateLastUpdatedTime.value = new Date(resp.data.last_updated_time);
      }
    });
    return getHealth
  }(), 10000)
})

onUnmounted(() => {
  clearInterval(timerId)
})

</script>
