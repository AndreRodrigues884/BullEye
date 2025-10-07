const mlService = require('../services/ml.service');
const { cache } = require('../config/redis');

class PredictionController {
  async getPrediction(req, res) {
    try {
      const { symbol } = req.params;
      const days = parseInt(req.query.days) || 1;

      // Check cache
      const cacheKey = `prediction:${symbol}:${days}`;
      const cached = await cache.get(cacheKey);

      if (cached) {
        return res.json({ ...cached, cached: true });
      }

      // Get from ML service
      const prediction = await mlService.getPrediction(symbol.toUpperCase(), days);

      // Cache for 15 minutes
      await cache.set(cacheKey, prediction, 900);

      res.json(prediction);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async getMultiDayPrediction(req, res) {
    try {
      const { symbol } = req.params;
      const days = parseInt(req.query.days) || 7;

      const cacheKey = `prediction:multi:${symbol}:${days}`;
      const cached = await cache.get(cacheKey);

      if (cached) {
        return res.json({ ...cached, cached: true });
      }

      const predictions = await mlService.getMultiDayPrediction(symbol.toUpperCase(), days);

      await cache.set(cacheKey, predictions, 900);

      res.json(predictions);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async batchPredictions(req, res) {
    try {
      const { symbols } = req.body;

      if (!symbols || !Array.isArray(symbols)) {
        return res.status(400).json({ error: 'Symbols array required' });
      }

      const predictions = await mlService.getBatchPredictions(
        symbols.map((s) => s.toUpperCase())
      );

      res.json(predictions);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = PredictionController;
