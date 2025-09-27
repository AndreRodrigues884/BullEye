<template>
  <div
    class="bg-gradient-to-br from-[#020826] to-[#090F30] rounded-3xl shadow-2xl p-6 w-full flex flex-col gap-4"
  >
    <!-- Cabeçalho -->
    <div class="flex items-center gap-3">
      <h3 class="text-gray-400 uppercase text-sm tracking-wider">Top Gainers</h3>
      <span class="ml-auto text-gray-400 text-sm">
        {{ topGainers?.length ?? 0 }} Stocks
      </span>
    </div>

    <!-- Tabela com scroll horizontal -->
    <div class="overflow-x-auto">
      <table class="min-w-[500px] w-full text-gray-200">
        <thead>
          <tr class="bg-[#090F30] text-gray-400 uppercase text-xs tracking-wider">
            <th class="px-4 py-2 text-left">Symbol</th>
            <th class="px-4 py-2 text-left">Name</th>
            <th class="px-4 py-2 text-left">Price</th>
            <th class="px-4 py-2 text-left">Change</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="stock in topGainers"
            :key="stock.symbol"
            class="border-b border-[#1A1F3D] hover:bg-[#0A132C] transition-colors"
          >
            <td class="px-4 py-2 flex items-center gap-2">
              <img
                v-if="stock.logo"
                :src="stock.logo"
                alt="Logo"
                class="w-6 h-6 rounded-full"
              />
              <span class="font-semibold text-white">{{ stock.symbol }}</span>
            </td>
            <td class="px-4 py-2">{{ stock.name }}</td>
            <td class="px-4 py-2 text-[#3B82F6]">
              ${{ stock.price ? stock.price.toFixed(2) : "-" }}
            </td>
            <td
              class="px-4 py-2 font-semibold"
              :class="stock.change >= 0 ? 'text-green-500' : 'text-red-500'"
            >
              {{ stock.change ? stock.change.toFixed(2) : "-" }}
              ({{ stock.change_pct ? stock.change_pct.toFixed(2) : "-" }}%)
            </td>
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
    const topGainers = computed(() => store.topGainers);
    return { topGainers };
  },
});
</script>
