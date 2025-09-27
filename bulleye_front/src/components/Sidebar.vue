<template>
  <aside class="w-40 h-screen bg-[#020826] text-white flex flex-col p-4">
    <!-- Logo / Título -->
    <div class="text-2xl font-bold mb-8">
      BullEye
    </div>

    <!-- Links de navegação -->
    <nav class="flex flex-col gap-3">
      <router-link
        to="/"
        class="px-4 py-2 rounded hover:bg-gray-800 transition-colors"
        active-class="bg-gray-800"
      >
        Overview
      </router-link>
      <router-link
        to="/stock-detail"
        class="px-4 py-2 rounded hover:bg-gray-800 transition-colors"
        active-class="bg-gray-800"
      >
        Stock Detail
      </router-link>
      <!-- Adicione mais links conforme necessário -->
    </nav>

    <!-- Rodapé da sidebar -->
    <div class="mt-auto text-sm text-gray-400">
      © 2025 BullEye
    </div>
  </aside>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Sidebar",
});
</script>
