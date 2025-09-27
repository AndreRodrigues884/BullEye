-- Extensão TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Tabela de usuários
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de símbolos de ações
CREATE TABLE stock_symbols (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    exchange VARCHAR(50),
    sector VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de dados históricos de ações (hypertable)
CREATE TABLE stock_data (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2),
    volume BIGINT,
    adjusted_close DECIMAL(10,2)
);

-- Converter para hypertable
SELECT create_hypertable('stock_data', 'time');

-- Tabela de previsões
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    prediction_date DATE NOT NULL,
    predicted_price DECIMAL(10,2),
    confidence_score DECIMAL(5,4),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_stock_data_symbol_time ON stock_data (symbol, time DESC);
CREATE INDEX idx_predictions_symbol_date ON predictions (symbol, prediction_date DESC);

-- Inserir alguns símbolos populares
INSERT INTO stock_symbols (symbol, name, exchange, sector) VALUES
('AAPL', 'Apple Inc.', 'NASDAQ', 'Technology'),
('MSFT', 'Microsoft Corporation', 'NASDAQ', 'Technology'),
('GOOGL', 'Alphabet Inc.', 'NASDAQ', 'Technology'),
('AMZN', 'Amazon.com Inc.', 'NASDAQ', 'Consumer Discretionary'),
('TSLA', 'Tesla Inc.', 'NASDAQ', 'Consumer Discretionary');