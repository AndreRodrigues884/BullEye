<template>
  <div class="p-6 bg-[#020826] rounded-2xl shadow-md w-full h-96 flex gap-6">
    <!-- Gráfico de Pizza: Market Weight -->
    <div class="flex-1 flex flex-col items-center justify-center">
      <h3 class="text-md font-semibold mb-2 text-[#D0D0D0]">Market Weight</h3>
      <apexchart
        type="pie"
        height="100%"
        width="100%"
        :series="marketSeries"
        :options="marketOptions"
      />
    </div>

    <!-- Gráfico de Linha: YTD Return -->
    <div class="flex-1 flex flex-col items-center justify-center">
      <h3 class="text-md font-semibold mb-2 text-[#D0D0D0]">YTD Return (%)</h3>
      <apexchart
        type="line"
        height="100%"
        width="650px"
        :series="ytdSeries"
        :options="ytdOptions"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import ApexCharts from "vue3-apexcharts";
import { useStocksStore } from "../store/stocks";

export default defineComponent({
  components: { apexchart: ApexCharts },
  setup() {
    const store = useStocksStore();

    // Protege contra topSectors undefined
    const sectors = computed(() => Array.isArray(store.topSectors) ? store.topSectors : []);

    // Pie chart: marketWeight
    const marketSeries = computed(() => sectors.value.map(s => s.marketWeight));
    const marketOptions = computed(() => ({
      labels: sectors.value.map(s => s.sector),
      colors: [
        '#4f46e5', '#6366f1', '#818cf8', '#a5b4fc', '#c7d2fe',
        '#22d3ee', '#06b6d4', '#3b82f6', '#2563eb', '#1e40af',
        '#9333ea', '#c026d3'
      ],
      legend: { labels: { colors: '#D0D0D0' }, position: 'bottom' },
      dataLabels: { style: { colors: ['#D0D0D0'] } },
      chart: { background: 'transparent', toolbar: { show: false } },
      tooltip: { theme: 'dark', y: { formatter: (val: number) => `${val.toFixed(2)}%` } },
    }));

    // Line chart: YTD Return
    const ytdSeries = computed(() => [
      { name: "YTD Return", data: sectors.value.map(s => s.ytdReturn) }
    ]);
    const ytdOptions = computed(() => ({
      chart: { toolbar: { show: false }, background: 'transparent', zoom: { enabled: false } },
      stroke: { curve: "smooth", width: 3 },
      xaxis: {
        categories: sectors.value.map(s => s.sector),
        labels: { rotate: -45, style: { colors: '#D0D0D0', fontSize: '12px' } },
      },
      yaxis: { labels: { style: { colors: '#D0D0D0', fontSize: '12px' } } },
      markers: { size: 5, colors: ['#4f46e5'], strokeColors: '#ffffff', strokeWidth: 2, hover: { size: 7 } },
      colors: ['#4f46e5'],
      grid: { borderColor: '#33375a', row: { colors: ['transparent'], opacity: 0.5 } },
      tooltip: { theme: 'dark', y: { formatter: (val: number) => `${val.toFixed(2)}%` } },
      legend: { show: false },
    }));

    return { marketSeries, marketOptions, ytdSeries, ytdOptions };
  },
});
</script>
