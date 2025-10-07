const { Router } = require('express');
const AuthController = require('../controllers/auth.controllers');
const { authMiddleware } = require('../middleware/auth.middleware');

const router = Router();
const authController = new AuthController();

router.post('/register', (req, res) => authController.register(req, res));
router.post('/login', (req, res) => authController.login(req, res));
router.get('/me', authMiddleware, (req, res) => authController.me(req, res));

module.exports = router;
