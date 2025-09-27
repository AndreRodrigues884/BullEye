export interface Stock {
  symbol: string;
  name: string;
  price: number;
  change: number;
  change_pct: number;
  volume: string;
  avgVolume?: string;
  marketCap?: string;
  peRatio?: number | null;
  wk52Change?: number;
  wk52Range?: [number, number];
  logo?: string;
}

export interface Sector {
  sector: string;
  marketWeight: number;
  ytdReturn: number;
}

export interface StocksState {
  topPick: Stock | null;
  topGainers: Stock[];
  topLosers: Stock[];
  topVolume: Stock[];
  topSectors: Sector[];
  loading: boolean;
  error: string | null;
}