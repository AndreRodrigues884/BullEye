<template>
  <div class="flex h-screen bg-[#090F30]">
    <!-- Sidebar fixa -->
    <Sidebar />

    <!-- Conteúdo principal scrollável -->
    <main class="flex-1 overflow-auto p-6">
      <router-view />
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Sidebar from "./components/Sidebar.vue";

export default defineComponent({
  components: { Sidebar },
});
</script>
