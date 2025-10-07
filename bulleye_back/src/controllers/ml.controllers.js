const mlService = require('../services/ml.service');

class MLController {
  async trainModel(req, res) {
    try {
      const { symbol, config } = req.body;

      if (!symbol) {
        return res.status(400).json({ error: 'Symbol required' });
      }

      const result = await mlService.trainModel(
        symbol.toUpperCase(),
        config || {}
      );

      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async listModels(req, res) {
    try {
      const models = await mlService.getModels();
      res.json(models);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async getEvaluation(req, res) {
    try {
      const { symbol } = req.params;
      const evaluation = await mlService.getModelEvaluation(symbol.toUpperCase());
      res.json(evaluation);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = MLController;
