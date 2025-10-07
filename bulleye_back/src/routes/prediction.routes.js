const { Router } = require('express');
const PredictionController = require('../controllers/prediction.controllers');
const { authMiddleware } = require('../middleware/auth.middleware');

const router = Router();
const predictionController = new PredictionController();

router.get('/:symbol', authMiddleware, (req, res) => 
  predictionController.getPrediction(req, res)
);

router.get('/:symbol/multi', authMiddleware, (req, res) => 
  predictionController.getMultiDayPrediction(req, res)
);

router.post('/batch', authMiddleware, (req, res) => 
  predictionController.batchPredictions(req, res)
);

module.exports = router;

