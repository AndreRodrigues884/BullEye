-- ============================================
-- BullEye Database - Init SQL (Ordem Correta)
-- ============================================

-- Limpa tudo (cuidado em produção!)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Extensões
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. USERS (sem dependências)
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ
);

CREATE INDEX idx_users_email ON users(email);

-- ============================================
-- 2. STOCK SYMBOLS (sem dependências)
-- ============================================
CREATE TABLE stock_symbols (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    exchange VARCHAR(50),
    currency VARCHAR(10) DEFAULT 'USD',
    sector VARCHAR(100),
    industry VARCHAR(100),
    country VARCHAR(100),
    market_cap BIGINT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_stock_symbols_symbol ON stock_symbols(symbol);
CREATE INDEX idx_stock_symbols_sector ON stock_symbols(sector);

-- ============================================
-- 3. USER WATCHLIST (depende de users e stock_symbols)
-- ============================================
CREATE TABLE user_watchlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL REFERENCES stock_symbols(symbol) ON DELETE CASCADE,
    notes TEXT,
    alert_price_above NUMERIC(12,4),
    alert_price_below NUMERIC(12,4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, symbol)
);

CREATE INDEX idx_watchlist_user ON user_watchlist(user_id);
CREATE INDEX idx_watchlist_symbol ON user_watchlist(symbol);

-- ============================================
-- 4. STOCK DATA (hypertable)
-- ============================================
CREATE TABLE stock_data (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    open NUMERIC(12,4) NOT NULL,
    high NUMERIC(12,4) NOT NULL,
    low NUMERIC(12,4) NOT NULL,
    close NUMERIC(12,4) NOT NULL,
    volume BIGINT NOT NULL,
    adjusted_close NUMERIC(12,4),
    dividend_amount NUMERIC(12,4) DEFAULT 0,
    split_coefficient NUMERIC(8,4) DEFAULT 1,
    
    CONSTRAINT valid_prices CHECK (
        open > 0 AND high > 0 AND low > 0 AND 
        close > 0 AND volume >= 0
    ),
    CONSTRAINT valid_high_low CHECK (high >= low),
    CONSTRAINT valid_ohlc CHECK (
        high >= open AND high >= close AND 
        low <= open AND low <= close
    )
);

-- Converter para hypertable
SELECT create_hypertable('stock_data', 'time', if_not_exists => TRUE);

-- Índices
CREATE INDEX idx_stock_data_symbol_time ON stock_data (symbol, time DESC);
CREATE INDEX idx_stock_data_time ON stock_data (time DESC);

-- Compressão (dados > 7 dias)
ALTER TABLE stock_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol'
);

SELECT add_compression_policy('stock_data', INTERVAL '7 days', if_not_exists => TRUE);

-- Retenção (manter 5 anos)
SELECT add_retention_policy('stock_data', INTERVAL '5 years', if_not_exists => TRUE);

-- ============================================
-- 5. TECHNICAL INDICATORS (hypertable)
-- ============================================
CREATE TABLE technical_indicators (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    sma_20 NUMERIC(12,4),
    sma_50 NUMERIC(12,4),
    sma_200 NUMERIC(12,4),
    ema_12 NUMERIC(12,4),
    ema_26 NUMERIC(12,4),
    rsi NUMERIC(5,2),
    macd NUMERIC(12,4),
    macd_signal NUMERIC(12,4),
    macd_hist NUMERIC(12,4),
    bb_upper NUMERIC(12,4),
    bb_middle NUMERIC(12,4),
    bb_lower NUMERIC(12,4),
    atr NUMERIC(12,4),
    obv BIGINT,
    PRIMARY KEY (time, symbol)
);

SELECT create_hypertable('technical_indicators', 'time', if_not_exists => TRUE);
CREATE INDEX idx_tech_indicators_symbol_time ON technical_indicators (symbol, time DESC);

-- ============================================
-- 6. PREDICTIONS
-- ============================================
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    prediction_date DATE NOT NULL,
    prediction_horizon INTEGER NOT NULL,
    predicted_price NUMERIC(12,4) NOT NULL,
    predicted_high NUMERIC(12,4),
    predicted_low NUMERIC(12,4),
    confidence_score NUMERIC(5,4) CHECK (confidence_score BETWEEN 0 AND 1),
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    features_used JSONB,
    metadata JSONB,
    actual_price NUMERIC(12,4),
    error_percentage NUMERIC(8,4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_prediction UNIQUE (symbol, prediction_date, prediction_horizon, model_version)
);

CREATE INDEX idx_predictions_symbol_date ON predictions (symbol, prediction_date DESC);
CREATE INDEX idx_predictions_created_at ON predictions (created_at DESC);
CREATE INDEX idx_predictions_model ON predictions (model_name, model_version);

-- ============================================
-- 7. MODEL PERFORMANCE
-- ============================================
CREATE TABLE model_performance (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    evaluation_date DATE NOT NULL,
    symbol VARCHAR(20),
    mse NUMERIC(12,6),
    rmse NUMERIC(12,6),
    mae NUMERIC(12,6),
    mape NUMERIC(8,4),
    r2_score NUMERIC(8,6),
    directional_accuracy NUMERIC(5,4),
    total_predictions INTEGER,
    training_samples INTEGER,
    training_time_seconds INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_model_eval UNIQUE (model_name, model_version, evaluation_date, symbol)
);

CREATE INDEX idx_model_perf_name_version ON model_performance (model_name, model_version);
CREATE INDEX idx_model_perf_date ON model_performance (evaluation_date DESC);

-- ============================================
-- 8. DATA COLLECTION LOGS
-- ============================================
CREATE TABLE data_collection_logs (
    id SERIAL PRIMARY KEY,
    collection_type VARCHAR(50) NOT NULL,
    symbols_requested TEXT[],
    symbols_success TEXT[],
    symbols_failed TEXT[],
    total_records INTEGER,
    duration_seconds INTEGER,
    error_message TEXT,
    status VARCHAR(20) DEFAULT 'success',
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_collection_logs_date ON data_collection_logs(completed_at DESC);
CREATE INDEX idx_collection_logs_status ON data_collection_logs(status);

-- ============================================
-- VIEWS
-- ============================================
CREATE OR REPLACE VIEW latest_stock_prices AS
SELECT DISTINCT ON (symbol)
    symbol,
    time,
    open,
    high,
    low,
    close,
    volume
FROM stock_data
ORDER BY symbol, time DESC;

CREATE OR REPLACE VIEW daily_stock_stats AS
SELECT 
    symbol,
    DATE(time) as date,
    FIRST(open, time) as open,
    MAX(high) as high,
    MIN(low) as low,
    LAST(close, time) as close,
    SUM(volume) as volume,
    COUNT(*) as data_points
FROM stock_data
GROUP BY symbol, DATE(time)
ORDER BY symbol, date DESC;

-- ============================================
-- FUNÇÕES ÚTEIS
-- ============================================
CREATE OR REPLACE FUNCTION calculate_return(
    start_price NUMERIC,
    end_price NUMERIC
) RETURNS NUMERIC AS $$
BEGIN
    IF start_price = 0 OR start_price IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN ((end_price - start_price) / start_price) * 100;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- DADOS INICIAIS
-- ============================================
INSERT INTO stock_symbols (symbol, name, exchange, sector, industry, country) VALUES
-- Tech Giants
('AAPL', 'Apple Inc.', 'NASDAQ', 'Technology', 'Consumer Electronics', 'USA'),
('MSFT', 'Microsoft Corporation', 'NASDAQ', 'Technology', 'Software', 'USA'),
('GOOGL', 'Alphabet Inc.', 'NASDAQ', 'Technology', 'Internet Services', 'USA'),
('AMZN', 'Amazon.com Inc.', 'NASDAQ', 'Consumer Discretionary', 'E-commerce', 'USA'),
('META', 'Meta Platforms Inc.', 'NASDAQ', 'Technology', 'Social Media', 'USA'),
('NVDA', 'NVIDIA Corporation', 'NASDAQ', 'Technology', 'Semiconductors', 'USA'),
('TSLA', 'Tesla Inc.', 'NASDAQ', 'Consumer Discretionary', 'Automotive', 'USA'),

-- Finance
('JPM', 'JPMorgan Chase & Co.', 'NYSE', 'Financials', 'Banking', 'USA'),
('BAC', 'Bank of America Corp.', 'NYSE', 'Financials', 'Banking', 'USA'),
('WFC', 'Wells Fargo & Company', 'NYSE', 'Financials', 'Banking', 'USA'),

-- Consumer
('WMT', 'Walmart Inc.', 'NYSE', 'Consumer Staples', 'Retail', 'USA'),
('COST', 'Costco Wholesale Corp.', 'NASDAQ', 'Consumer Staples', 'Retail', 'USA'),
('HD', 'The Home Depot Inc.', 'NYSE', 'Consumer Discretionary', 'Home Improvement', 'USA'),

-- Healthcare
('JNJ', 'Johnson & Johnson', 'NYSE', 'Healthcare', 'Pharmaceuticals', 'USA'),
('UNH', 'UnitedHealth Group Inc.', 'NYSE', 'Healthcare', 'Healthcare Plans', 'USA'),
('PFE', 'Pfizer Inc.', 'NYSE', 'Healthcare', 'Pharmaceuticals', 'USA')

ON CONFLICT (symbol) DO NOTHING;

-- ============================================
-- MENSAGEM FINAL
-- ============================================
DO $$
BEGIN
    RAISE NOTICE '✅ BullEye database initialized successfully!';
    RAISE NOTICE 'Tables created: %, Views: %, Functions: %', 
        (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'),
        (SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public'),
        (SELECT COUNT(*) FROM information_schema.routines WHERE routine_schema = 'public');
END $$;