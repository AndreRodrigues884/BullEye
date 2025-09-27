<template>
  <div
    class="bg-gradient-to-br from-[#020826] to-[#090F30] rounded-3xl shadow-2xl p-6 w-full flex flex-col gap-4"
  >
    <!-- Cabeçalho -->
    <div class="flex items-center gap-3">
      <h3 class="text-gray-400 uppercase text-sm tracking-wider">Top Volume</h3>
      <span class="ml-auto text-gray-400 text-sm">
        {{ topVolume?.length ?? 0 }} Stocks
      </span>
    </div>

    <!-- Tabela com scroll horizontal -->
    <div class="overflow-x-auto">
      <table class="min-w-[600px] w-full text-gray-200">
        <thead>
          <tr class="bg-[#090F30] text-gray-400 uppercase text-xs tracking-wider">
            <th class="px-4 py-2 text-left">Symbol</th>
            <th class="px-4 py-2 text-left">Name</th>
            <th class="px-4 py-2 text-left">Price</th>
            <th class="px-4 py-2 text-left">Volume</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="stock in topVolume"
            :key="stock.symbol"
            class="border-b border-[#1A1F3D] hover:bg-[#0A132C] transition-colors"
          >
            <td class="px-4 py-2 font-semibold text-white">
              {{ stock.symbol }}
            </td>
            <td class="px-4 py-2">{{ stock.name }}</td>
            <td class="px-4 py-2 text-[#3B82F6]">
              ${{ stock.price ? stock.price.toFixed(2) : "-" }}
            </td>
            <td class="px-4 py-2">{{ stock.volume ?? "-" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent, computed } from "vue";
import { useStocksStore } from "../store/stocks";

export default defineComponent({
  setup() {
    const store = useStocksStore();
    const topVolume = computed(() => store.topVolume);
    return { topVolume };
  },
});
</script>
