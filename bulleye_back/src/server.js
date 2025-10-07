// backend/src/server.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');
const dotenv = require('dotenv');

dotenv.config();

// Routes
const authRoutes = require('./routes/auth.routes');
const stockRoutes = require('./routes/stock.routes');
const predictionRoutes = require('./routes/prediction.routes');
const mlRoutes = require('./routes/ml.routes');
const userRoutes = require('./routes/user.routes');

const app = express();

// ============================================
// MIDDLEWARES
// ============================================

app.use(helmet());

app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(morgan('dev'));

// Rate limiting global
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // limite por IP
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// Rate limiting estrito (ex: login)
const strictLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  message: 'Too many requests, please try again later.'
});

// ============================================
// ROUTES
// ============================================

app.get('/', (req, res) => {
  res.json({
    service: 'BullEye Backend API',
    version: '2.0.0',
    status: 'running',
    endpoints: {
      auth: '/api/auth/*',
      stocks: '/api/stocks/*',
      predictions: '/api/predictions/*',
      ml: '/api/ml/*',
      user: '/api/user/*'
    }
  });
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// API Routes
app.use('/api/auth', strictLimiter, authRoutes);
app.use('/api/stocks', stockRoutes);
app.use('/api/predictions', predictionRoutes);
app.use('/api/ml', mlRoutes);
app.use('/api/user', userRoutes);

// 404 Handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: `Route ${req.originalUrl} not found`
  });
});

// Error Handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});

// ============================================
// START SERVER
// ============================================

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🚀 BullEye Backend running on port ${PORT}`);
  console.log(`📚 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔗 ML Service: ${process.env.ML_SERVICE_URL}`);
});

module.exports = app;
