<template>
    <div class="absolute w-screen h-screen left-0 top-0 flex flex-col justify-center backdrop-blur-sm" v-if="popups.length != 0">>
        <div class="mx-auto w-fit h-fit">
            <ConfirmPopup v-if="popups[0].type == 'confirm' " :params="popups[0].params"/>
        </div>
    </div>
</template>

<script setup>
import { usePopup } from '@/stores/popups';
import { storeToRefs } from 'pinia';
import ConfirmPopup from './general/ConfirmPopup.vue';


const popupStore = usePopup();
const { popups } = storeToRefs(popupStore)
</script>