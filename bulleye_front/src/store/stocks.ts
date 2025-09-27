import { defineStore } from "pinia";
import { Stock, Sector, StocksState } from "../types/types";
import { fetchTopPick, fetchTopGainers, fetchTopLosers, fetchTopVolume, fetchTopSectors } from "../api/stock";

export const useStocksStore = defineStore("stocks", {
  state: (): StocksState => ({
    topPick: null,
    topGainers: [],
    topLosers: [],
    topVolume: [],
    topSectors: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchStocks() {
      this.loading = true;
      this.error = null;

      try {
        // Chama as funções do api/stocks.ts
        const [pickRes, gainersRes, losersRes, volumeRes, sectorsRes] = await Promise.all([
          fetchTopPick(),
          fetchTopGainers(),
          fetchTopLosers(),
          fetchTopVolume(),
          fetchTopSectors(),
        ]);

        this.topPick = pickRes.data;
        this.topGainers = gainersRes.data;
        this.topLosers = losersRes.data;
        this.topVolume = volumeRes.data;
        this.topSectors = sectorsRes.data;
      } catch (err: any) {
        this.error = err?.message || "Erro ao buscar dados das stocks";
      } finally {
        this.loading = false;
      }
    },
  },
});
