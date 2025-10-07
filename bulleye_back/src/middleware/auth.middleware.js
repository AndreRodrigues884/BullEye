const jwt = require('jsonwebtoken');
const db = require('../config/database');

// Middleware de autenticação
const authMiddleware = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');

    if (!token) {
      res.status(401).json({ error: 'No token, authorization denied' });
      return;
    }

    // Verifica o token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    if (!decoded || !decoded.userId) {
      res.status(401).json({ error: 'Invalid token payload' });
      return;
    }

    // Busca o usuário no banco de dados
    const result = await db.query(
      'SELECT id, uuid, email, username, role FROM users WHERE id = $1 AND is_active = true',
      [decoded.userId]
    );

    if (result.rows.length === 0) {
      res.status(401).json({ error: 'User not found or inactive' });
      return;
    }

    // Adiciona o usuário ao request
    req.user = result.rows[0];
    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      res.status(401).json({ error: 'Invalid token' });
      return;
    }
    if (error.name === 'TokenExpiredError') {
      res.status(401).json({ error: 'Token expired' });
      return;
    }

    console.error('Auth middleware error:', error);
    res.status(500).json({ error: 'Server error' });
  }
};

// Middleware de admin
const adminMiddleware = (req, res, next) => {
  if (!req.user || req.user.role !== 'admin') {
    res.status(403).json({ error: 'Admin access required' });
    return;
  }
  next();
};

module.exports = { authMiddleware, adminMiddleware };
