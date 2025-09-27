<template>
  <div
    v-if="topPick"
    class="bg-gradient-to-br from-[#020826] to-[#090F30] rounded-3xl shadow-2xl p-6 w-full flex flex-col gap-6"
  >
    <!-- Cabeçalho com logo e nome -->
    <div class="flex items-center gap-4">
      <img
        :src="topPick.logo"
        alt="Logo"
        class="w-10 h-10 rounded-full border-2 border-[#4E4E4E]"
      />
      <div>
        <p class="text-gray-400 uppercase text-sm tracking-wider">Top Pick</p>
        <p class="text-white font-bold text-xl">
          {{ topPick.symbol }} - {{ topPick.name }}
        </p>
      </div>
    </div>

    <!-- Informações principais -->
    <div class="flex flex-wrap gap-6">
      <div class="flex flex-col">
        <span class="text-gray-400 text-sm">Price</span>
        <span class="text-white font-semibold text-lg">
          ${{ topPick?.price?.toFixed(2) ?? "-" }}
        </span>
      </div>

      <div class="flex flex-col">
        <span class="text-gray-400 text-sm">Change</span>
        <span
          :class="
            topPick?.change >= 0
              ? 'text-green-400 font-semibold'
              : 'text-red-500 font-semibold'
          "
        >
          {{ topPick?.change?.toFixed(2) ?? "-" }} ({{
            topPick?.change_pct?.toFixed(2) ?? "-"
          }}%)
        </span>
      </div>

      <div class="flex flex-col">
        <span class="text-gray-400 text-sm">Volume</span>
        <span class="text-white font-semibold">
          {{ topPick?.volume ?? "-" }}
        </span>
      </div>

      <div v-if="topPick?.marketCap" class="flex flex-col">
        <span class="text-gray-400 text-sm">Market Cap</span>
        <span class="text-white font-semibold">
          {{ topPick.marketCap }}
        </span>
      </div>
    </div>

    <!-- Gráfico ApexCharts -->
    <div class="mt-4">
      <apexchart
        type="line"
        :series="series"
        :options="chartOptions"
        height="320"
        class="rounded-xl bg-[#0A132C] p-2"
      />
    </div>
  </div>

  <LoadingSpinner v-else />
</template>


<script lang="ts">
import { defineComponent, computed } from "vue";
import { useStocksStore } from "../store/stocks";
import LoadingSpinner from "./LoadingSpinner.vue";
import ApexCharts from "vue3-apexcharts";
import intcLogo from '../assets/logos/intc.png';

export default defineComponent({
  components: { LoadingSpinner, apexchart: ApexCharts },
  setup() {
    const store = useStocksStore();

    // Mapa de logos
    const logos: Record<string, string> = {
      INTC: intcLogo,
      // adicione outros logos aqui
    };

    // topPick com logo resolvido
    const topPick = computed(() => {
      const pick = store.topPick;
      if (!pick) return null;

      return {
        ...pick,
        logo: logos[pick.symbol] || '', // pega o logo correto
      };
    });

    // Dados do gráfico (simulação para exemplo)
    const series = computed(() => [
      {
        name: "Price",
        data: topPick.value
          ? [
            topPick.value.price * 0.95,
            topPick.value.price * 0.98,
            topPick.value.price * 1.02,
            topPick.value.price,
            topPick.value.price * 1.05,
          ]
          : [],
      },
    ]);

    const chartOptions = {
      chart: {
        toolbar: { show: false },
        foreColor: "#D0D0D0",
      },
      stroke: { curve: "smooth", width: 3 },
      grid: { borderColor: "#1A1F3D", row: { colors: ["transparent"], opacity: 0.2 } },
      xaxis: { categories: ["Mon", "Tue", "Wed", "Thu", "Fri"], labels: { style: { colors: "#A0A0A0" } } },
      yaxis: { labels: { style: { colors: "#A0A0A0" } } },
      tooltip: { theme: "dark" },
      colors: ["#1F8B30"],
    };

    return { topPick, series, chartOptions };
  },
});
</script>

