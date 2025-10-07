const { Router } = require('express');
const StockController = require('../controllers/stock.controllers');
const { authMiddleware } = require('../middleware/auth.middleware');

const router = Router();
const stockController = new StockController();

router.get('/', (req, res) => stockController.listStocks(req, res));

router.get('/:symbol', authMiddleware, (req, res) => 
  stockController.getStockData(req, res)
);

router.get('/:symbol/analysis', authMiddleware, (req, res) => 
  stockController.getStockAnalysis(req, res)
);

router.post('/update', authMiddleware, (req, res) => 
  stockController.updateStockData(req, res)
);

module.exports = router;
