<template>
  <div class="spinner">
    <div class="bounce1"></div>
    <div class="bounce2"></div>
    <div class="bounce3"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({});
</script>

<style scoped>
.spinner {
  margin: 2rem auto;
  width: 70px;
  text-align: center;
}
.spinner > div {
  width: 18px;
  height: 18px;
  background-color: #4f46e5;
  border-radius: 100%;
  display: inline-block;
  animation: bouncedelay 1.4s infinite ease-in-out both;
}
.spinner .bounce1 { animation-delay: -0.32s; }
.spinner .bounce2 { animation-delay: -0.16s; }
@keyframes bouncedelay {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}
</style>
