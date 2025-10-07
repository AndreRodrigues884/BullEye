const { Router } = require('express');
const MLController = require('../controllers/ml.controllers');
const { authMiddleware, adminMiddleware } = require('../middleware/auth.middleware');

const router = Router();
const mlController = new MLController();

router.post(
  '/train',
  authMiddleware,
  adminMiddleware,
  (req, res) => mlController.trainModel(req, res)
);

router.get(
  '/models',
  authMiddleware,
  (req, res) => mlController.listModels(req, res)
);

router.get(
  '/evaluation/:symbol',
  authMiddleware,
  (req, res) => mlController.getEvaluation(req, res)
);

module.exports = router;
