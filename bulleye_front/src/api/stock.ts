import axios from "axios";

const API_BASE = "http://localhost:4000/api/stocks";

export const fetchTopPick = () => axios.get(`${API_BASE}/top-pick`);
export const fetchTopGainers = () => axios.get(`${API_BASE}/top-gainers`);
export const fetchTopLosers = () => axios.get(`${API_BASE}/top-losers`);
export const fetchTopVolume = () => axios.get(`${API_BASE}/top-volume`);
export const fetchTopSectors = () => axios.get(`${API_BASE}/top-sectors`);
