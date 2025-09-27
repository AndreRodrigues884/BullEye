/* import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const API_BASE = "http://api.marketstack.com/v1";
const API_KEY = process.env.MARKETSTACK_KEY;

// Cache simples em memória
let topPickCache: { data: any; timestamp: number } | null = null;
let topVolumeCache: { data: any; timestamp: number } | null = null;
let topGainersCache: { data: any; timestamp: number } | null = null;
let topSectorsCache: { data: any; timestamp: number } | null = null;
const CACHE_DURATION = 10 * 60 * 1000; // 10 minutos

const tickers = [
  "AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "META", "NVDA",
  "NFLX", "ADBE", "INTC", "ORCL", "CSCO", "IBM", "BABA"
];

const tickersWithSectors = [
  { symbol: "AAPL", sector: "Technology" },
  { symbol: "MSFT", sector: "Technology" },
  { symbol: "TSLA", sector: "Automotive" },
  { symbol: "GOOGL", sector: "Technology" },
  { symbol: "AMZN", sector: "Consumer Discretionary" },
  { symbol: "META", sector: "Technology" },
  { symbol: "NVDA", sector: "Technology" },
  { symbol: "NFLX", sector: "Communication Services" },
  { symbol: "ADBE", sector: "Technology" },
  { symbol: "INTC", sector: "Technology" },
];




// Fetch stocks with the highest percentage gain
export const fetchTopGainers = async () => {
  if (topGainersCache && Date.now() - topGainersCache.timestamp < CACHE_DURATION) {
    return topGainersCache.data;
  }

  try {
    const res = await axios.get(`${API_BASE}/eod`, {
      params: { access_key: API_KEY, symbols: tickers.join(","), limit: 1 },
    });

    const data = res.data.data.map((d: any) => ({
      symbol: d.symbol,
      open: d.open,
      close: d.close,
      change_pct: ((d.close - d.open) / d.open) * 100,
      volume: d.volume,
    }));

    const topGainers = data.sort((a: any, b: any) => b.change_pct - a.change_pct).slice(0, 10);

    topGainersCache = { data: topGainers, timestamp: Date.now() };
    return topGainers;
  } catch (err) {
    console.error("Erro fetchTopGainers:", err);
    return [];
  }
};
// Fetch stocks with the highest trading volume
export const fetchTopVolume = async () => {
  if (topVolumeCache && Date.now() - topVolumeCache.timestamp < CACHE_DURATION) {
    return topVolumeCache.data;
  }

  try {
    const res = await axios.get(`${API_BASE}/eod`, {
      params: { access_key: API_KEY, symbols: tickers.join(","), limit: 1 },
    });

    const data = res.data.data.map((d: any) => ({
      symbol: d.symbol,
      open: d.open,
      close: d.close,
      volume: d.volume,
      change_pct: ((d.close - d.open) / d.open) * 100,
    }));

    const topVolume = data.sort((a: any, b: any) => b.volume - a.volume).slice(0, 10);

    topVolumeCache = { data: topVolume, timestamp: Date.now() };
    return topVolume;
  } catch (err) {
    console.error("Erro fetchTopVolume:", err);
    return [];
  }
};
// Fetch the stock with the highest percentage gain
export const fetchTopPick = async () => {
  // Retorna do cache se ainda válido
  if (topPickCache && Date.now() - topPickCache.timestamp < CACHE_DURATION) {
    return topPickCache.data;
  }

  const topPickArray: any[] = [];

  for (const symbol of tickers) {
    try {
      const res = await axios.get(`${API_BASE}/eod`, {
        params: { access_key: API_KEY, symbols: symbol, limit: 1 }
      });
      const d = res.data.data[0];
      if (d) {
        topPickArray.push({
          symbol: d.symbol,
          close: d.close,
          open: d.open,
          change_pct: ((d.close - d.open) / d.open) * 100
        });
      }
      // Pequeno delay para não exceder rate limit
      await new Promise(r => setTimeout(r, 500));
    } catch (err) {
      console.error(`Erro ao buscar ${symbol}:`, err);
    }
  }

  // Ordena e pega o top pick
  const topPick = topPickArray.sort((a, b) => b.change_pct - a.change_pct)[0];

  // Armazena no cache
  topPickCache = { data: topPick, timestamp: Date.now() };

  return topPick;
};

// Fetch sectors with the highest average percentage gain
export const fetchTopSectors = async () => {
  // Retorna do cache se válido
  if (topSectorsCache && Date.now() - topSectorsCache.timestamp < CACHE_DURATION) {
    return topSectorsCache.data;
  }

  const sectorMap: Record<string, { total: number; count: number }> = {};

  for (const t of tickersWithSectors) {
    try {
      const res = await axios.get(`${API_BASE}/eod`, {
        params: { access_key: API_KEY, symbols: t.symbol, limit: 1 }
      });
      const d = res.data.data[0];
      if (d) {
        const change_pct = ((d.close - d.open) / d.open) * 100;
        if (!sectorMap[t.sector]) sectorMap[t.sector] = { total: 0, count: 0 };
        sectorMap[t.sector].total += change_pct;
        sectorMap[t.sector].count += 1;
      }

      // Pequeno delay para não estourar rate limit
      await new Promise(r => setTimeout(r, 500));
    } catch (err) {
      console.error(`Erro ao buscar ${t.symbol}:`, err);
    }
  }

  const sectors = Object.entries(sectorMap).map(([sector, val]) => ({
    sector,
    avg_change_pct: val.total / val.count,
  }));

  // Ordena do maior para o menor
  const result = sectors.sort((a, b) => b.avg_change_pct - a.avg_change_pct);

  // Salva no cache
  topSectorsCache = { data: result, timestamp: Date.now() };

  return result;
};
 */