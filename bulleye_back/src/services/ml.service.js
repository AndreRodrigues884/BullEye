const axios = require('axios');

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://ml-service:8000';

class MLService {
  // ==============================
  // 🔮 Predictions
  // ==============================
  async getPrediction(symbol, daysAhead = 1) {
    try {
      const response = await axios.post(
        `${ML_SERVICE_URL}/api/predict`,
        { symbol, days_ahead: daysAhead },
        { timeout: 30000 }
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getBatchPredictions(symbols) {
    try {
      const response = await axios.post(
        `${ML_SERVICE_URL}/api/predict/batch`,
        { symbols },
        { timeout: 60000 }
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getMultiDayPrediction(symbol, days) {
    try {
      const response = await axios.get(
        `${ML_SERVICE_URL}/api/predict/${symbol}/multi?days=${days}`,
        { timeout: 30000 }
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // ==============================
  // 🧠 Model Management
  // ==============================
  async trainModel(symbol, config = {}) {
    try {
      const response = await axios.post(
        `${ML_SERVICE_URL}/api/train`,
        {
          symbol,
          sequence_length: config.sequenceLength || 60,
          prediction_horizon: config.predictionHorizon || 1,
          epochs: config.epochs || 100,
          validation_split: config.validationSplit || 0.2
        },
        { timeout: 600000 } // 10 minutos
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getModels() {
    try {
      const response = await axios.get(`${ML_SERVICE_URL}/api/models`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getModelEvaluation(symbol) {
    try {
      const response = await axios.get(`${ML_SERVICE_URL}/api/evaluation/${symbol}`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // ==============================
  // 📊 Data Management
  // ==============================
  async collectData(symbols, period = '1y', interval = '1d') {
    try {
      const response = await axios.post(
        `${ML_SERVICE_URL}/api/data/collect`,
        { symbols, period, interval },
        { timeout: 300000 } // 5 minutos
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getStockData(symbol, params = {}) {
    try {
      const queryParams = new URLSearchParams(params).toString();
      const response = await axios.get(
        `${ML_SERVICE_URL}/api/data/stocks/${symbol}?${queryParams}`
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getStockAnalysis(symbol) {
    try {
      const response = await axios.get(
        `${ML_SERVICE_URL}/api/data/stocks/${symbol}/analysis`
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async listStocks() {
    try {
      const response = await axios.get(`${ML_SERVICE_URL}/api/data/stocks`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // ==============================
  // ❤️ Health Check
  // ==============================
  async healthCheck() {
    try {
      const response = await axios.get(`${ML_SERVICE_URL}/health`, { timeout: 5000 });
      return response.data;
    } catch (error) {
      return { status: 'unhealthy', error: error.message };
    }
  }

  // ==============================
  // ⚠️ Error Handling
  // ==============================
  handleError(error) {
    if (error.response) {
      const data = error.response.data;
      return new Error(data.detail || data.error || 'ML service error');
    } else if (error.request) {
      return new Error('ML service unavailable');
    } else {
      return new Error(error.message);
    }
  }
}

module.exports = new MLService();
