import { Request, Response } from "express";
import { topPick, trendingNow, topGainers, topLosers, sectors } from "../data/stockData";

// Retorna o Top Pick
export const getTopPick = (req: Request, res: Response) => {
  res.json(topPick);
};

// Retorna as 10 stocks com maior volume
export const getTopVolume = (req: Request, res: Response) => {
  const sorted = [...trendingNow].sort((a, b) => {
    const parseVolume = (v: string) => {
      if (v.endsWith("M")) return parseFloat(v) * 1_000_000;
      if (v.endsWith("k")) return parseFloat(v) * 1_000;
      return parseFloat(v);
    };
    return parseVolume(b.volume) - parseVolume(a.volume);
  });
  res.json(sorted.slice(0, 10));
};

// Retorna os Top Gainers
export const getTopGainers = (req: Request, res: Response) => {
  res.json(topGainers.slice(0, 10));
};

// Retorna os Top Losers
export const getTopLosers = (req: Request, res: Response) => {
  res.json(topLosers.slice(0, 10));
};

// Retorna os Top 5 setores (por marketWeight)
export const getTopSectors = (req: Request, res: Response) => {
  const sorted = [...sectors].sort((a, b) => b.marketWeight - a.marketWeight);
  res.json(sorted.slice(0, 11));
};