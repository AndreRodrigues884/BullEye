<template>
  <div class="flex flex-col gap-8 p-8">
    <!-- Top Pick e Top Gainers lado a lado -->
    <div class="flex flex-wrap gap-6">
      <!-- Top Pick maior -->
      <TopPickCard class="flex-[2] min-w-[600px]" />

      <!-- Top Gainers menor -->
       <TopVolumeTable class="flex-1 min-w-[300px]" />
      
    </div>

    <!-- Top Losers e Top Volume em grid responsivo -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <TopGainersTable />
      <TopLosersTable />
    </div>

    <!-- Top Sectors Chart -->
    <TopSectorsChart />
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useStocksStore } from "../store/stocks";

import TopPickCard from "../components/TopPickCard.vue";
import TopGainersTable from "../components/TopGainersTable.vue";
import TopLosersTable from "../components/TopLosersTable.vue";
import TopVolumeTable from "../components/TopVolumeTable.vue";
import TopSectorsChart from "../components/TopSectorsChart.vue";

export default defineComponent({
  components: {
    TopPickCard,
    TopGainersTable,
    TopLosersTable,
    TopVolumeTable,
    TopSectorsChart,
  },
  setup() {
    const store = useStocksStore();
    onMounted(() => store.fetchStocks());
  },
});
</script>
