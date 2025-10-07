const mlService = require('../services/ml.service');
const { cache } = require('../config/redis');

class StockController {
  async listStocks(req, res) {
    try {
      const cacheKey = 'stocks:all';
      const cached = await cache.get(cacheKey);

      if (cached) {
        return res.json({ ...cached, cached: true });
      }

      const stocks = await mlService.listStocks();

      await cache.set(cacheKey, stocks, 3600);

      res.json(stocks);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async getStockData(req, res) {
    try {
      const { symbol } = req.params;
      const { start_date, end_date, limit } = req.query;

      const cacheKey = `stock:${symbol}:${start_date}:${end_date}:${limit}`;
      const cached = await cache.get(cacheKey);

      if (cached) {
        return res.json({ ...cached, cached: true });
      }

      const data = await mlService.getStockData(symbol.toUpperCase(), {
        start_date,
        end_date,
        limit
      });

      await cache.set(cacheKey, data, 1800);

      res.json(data);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async getStockAnalysis(req, res) {
    try {
      const { symbol } = req.params;

      const cacheKey = `analysis:${symbol}`;
      const cached = await cache.get(cacheKey);

      if (cached) {
        return res.json({ ...cached, cached: true });
      }

      const analysis = await mlService.getStockAnalysis(symbol.toUpperCase());

      await cache.set(cacheKey, analysis, 3600);

      res.json(analysis);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async updateStockData(req, res) {
    try {
      const { symbols, period, interval } = req.body;

      if (!symbols || !Array.isArray(symbols)) {
        return res.status(400).json({ error: 'Symbols array required' });
      }

      const result = await mlService.collectData(
        symbols.map((s) => s.toUpperCase()),
        period || '1y',
        interval || '1d'
      );

      // Clear cache
      for (const symbol of symbols) {
        await cache.del(`stock:${symbol}*`);
        await cache.del(`prediction:${symbol}*`);
      }

      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = StockController;
