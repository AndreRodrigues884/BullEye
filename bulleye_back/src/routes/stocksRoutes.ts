import { Router } from "express";
import { getTopGainers, getTopVolume, getTopPick, getTopSectors, getTopLosers } from "../controllers/stocksController";

const router = Router();

// Aqui só definimos endpoints e middlewares (como auth, se houver)
router.get("/top-pick", getTopPick);
router.get("/top-volume", getTopVolume);
router.get("/top-gainers", getTopGainers);
router.get("/top-losers", getTopLosers);
router.get("/top-sectors", getTopSectors);

export default router;
