<template>
  <div class="stock-detail" v-if="stock">
    <h2>{{ stock.symbol }} - {{ stock.name }}</h2>
    <p>Price: ${{ stock.price.toFixed(2) }}</p>
    <p :class="{positive: stock.change>=0, negative: stock.change<0}">
      Change: {{ stock.change }} ({{ stock.change_pct }}%)
    </p>
    <p>Volume: {{ stock.volume }}</p>
    <p v-if="stock.marketCap">Market Cap: {{ stock.marketCap }}</p>

    <canvas ref="chart"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default defineComponent({
  setup() {
    const route = useRoute();
    const stock = ref<any>(null);
    const chartRef = ref<HTMLCanvasElement | null>(null);

    const fetchStock = async () => {
      const res = await axios.get(`http://localhost:4000/api/stocks/top-pick`); // Exemplo
      stock.value = res.data;
      renderChart();
    };

    const renderChart = () => {
      if (!chartRef.value || !stock.value) return;
      const ctx = chartRef.value.getContext("2d");
      if (!ctx) return;

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['-5d','-4d','-3d','-2d','-1d','Today'],
          datasets: [{
            label: 'Price',
            data: [33,34,34.5,35,34.8,stock.value.price],
            borderColor: '#4f46e5',
            backgroundColor: 'rgba(79,70,229,0.2)',
            fill: true,
            tension: 0.3
          }]
        },
        options: { responsive: true }
      });
    };

    onMounted(fetchStock);

    return { stock, chartRef };
  }
});
</script>

<style scoped>
.stock-detail {
  padding: 2rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.positive { color: green; }
.negative { color: red; }
</style>
