// src/router/index.ts
import { createRouter, createWebHashHistory } from "vue-router";
import Overview from "../pages/Overview.vue";
import StockDetail from "../pages/StockDetail.vue";

const routes = [
  {
    path: "/",
    name: "Overview",
    component: Overview,
  },
  {
    path: "/stock/:symbol",
    name: "StockDetail",
    component: StockDetail,
    props: true, // permite passar o ticker como prop
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
