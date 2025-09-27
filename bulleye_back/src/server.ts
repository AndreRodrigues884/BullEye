import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import stocksRouter from "./routes/stocksRoutes";
import path from "path";

dotenv.config();
const app = express();

app.use(cors());
app.use(express.json());

app.use('/assets', express.static(path.join(__dirname, '../assets')));

// rotas
app.use("/api/stocks", stocksRouter);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});
