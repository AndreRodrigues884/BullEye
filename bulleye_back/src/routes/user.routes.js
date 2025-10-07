const { Router } = require('express');
const UserController = require('../controllers/user.controllers');
const { authMiddleware } = require('../middleware/auth.middleware');

const router = Router();
const userController = new UserController();

router.get('/watchlist', authMiddleware, (req, res) => 
  userController.getWatchlist(req, res)
);

router.post('/watchlist', authMiddleware, (req, res) => 
  userController.addToWatchlist(req, res)
);

router.delete('/watchlist/:symbol', authMiddleware, (req, res) => 
  userController.removeFromWatchlist(req, res)
);

module.exports = router;
