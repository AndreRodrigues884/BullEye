# ml-service/main.py
# API FastAPI com endpoints REST (/collect, /stocks, /stocks/{symbol}/data, etc)
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import logging
from data_collector import StockDataCollector
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BullEye ML Service",
    description="Machine Learning service for stock market predictions",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url)


# Models
class CollectionRequest(BaseModel):
    symbols: List[str]
    period: str = "1y"
    interval: str = "1d"


class StockDataResponse(BaseModel):
    symbol: str
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class CollectionStatus(BaseModel):
    status: str
    message: str
    details: Optional[dict] = None


# Routes
@app.get("/")
async def root():
    return {
        "service": "BullEye ML Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Testar conexão com banco
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.post("/collect", response_model=CollectionStatus)
async def collect_data(
    request: CollectionRequest,
    background_tasks: BackgroundTasks
):
    """
    Inicia coleta de dados para os símbolos especificados
    A coleta é feita em background
    """
    try:
        collector = StockDataCollector()
        
        # Executar em background
        background_tasks.add_task(
            collector.collect_multiple_stocks,
            request.symbols,
            request.period,
            request.interval
        )
        
        return CollectionStatus(
            status="started",
            message=f"Data collection started for {len(request.symbols)} stocks",
            details={
                "symbols": request.symbols,
                "period": request.period,
                "interval": request.interval
            }
        )
        
    except Exception as e:
        logger.error(f"Error starting collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stocks")
async def list_stocks():
    """Lista todas as ações disponíveis no banco"""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT symbol, name, exchange, sector, created_at
                FROM stock_symbols
                ORDER BY symbol
            """)
            result = conn.execute(query)
            
            stocks = []
            for row in result:
                stocks.append({
                    'symbol': row[0],
                    'name': row[1],
                    'exchange': row[2],
                    'sector': row[3],
                    'created_at': row[4].isoformat() if row[4] else None
                })
            
            return {
                "count": len(stocks),
                "stocks": stocks
            }
            
    except Exception as e:
        logger.error(f"Error listing stocks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stocks/{symbol}/data")
async def get_stock_data(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100
):
    """
    Retorna dados históricos de uma ação
    
    Args:
        symbol: Símbolo da ação
        start_date: Data inicial (YYYY-MM-DD)
        end_date: Data final (YYYY-MM-DD)
        limit: Número máximo de registros
    """
    try:
        symbol = symbol.upper()
        
        # Construir query
        query_str = """
            SELECT time, symbol, open, high, low, close, volume
            FROM stock_data
            WHERE symbol = :symbol
        """
        
        params = {'symbol': symbol}
        
        if start_date:
            query_str += " AND time >= :start_date"
            params['start_date'] = start_date
            
        if end_date:
            query_str += " AND time <= :end_date"
            params['end_date'] = end_date
        
        query_str += " ORDER BY time DESC LIMIT :limit"
        params['limit'] = limit
        
        with engine.connect() as conn:
            result = conn.execute(text(query_str), params)
            
            data = []
            for row in result:
                data.append({
                    'time': row[0].isoformat(),
                    'symbol': row[1],
                    'open': float(row[2]),
                    'high': float(row[3]),
                    'low': float(row[4]),
                    'close': float(row[5]),
                    'volume': int(row[6])
                })
            
            if not data:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data found for symbol {symbol}"
                )
            
            return {
                "symbol": symbol,
                "count": len(data),
                "data": list(reversed(data))  # Ordem cronológica
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stocks/{symbol}/latest")
async def get_latest_price(symbol: str):
    """Retorna o último preço disponível de uma ação"""
    try:
        symbol = symbol.upper()
        
        with engine.connect() as conn:
            query = text("""
                SELECT time, open, high, low, close, volume
                FROM stock_data
                WHERE symbol = :symbol
                ORDER BY time DESC
                LIMIT 1
            """)
            result = conn.execute(query, {'symbol': symbol}).fetchone()
            
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data found for symbol {symbol}"
                )
            
            return {
                'symbol': symbol,
                'time': result[0].isoformat(),
                'open': float(result[1]),
                'high': float(result[2]),
                'low': float(result[3]),
                'close': float(result[4]),
                'volume': int(result[5])
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching latest price: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stocks/{symbol}/stats")
async def get_stock_statistics(symbol: str, days: int = 30):
    """
    Retorna estatísticas de uma ação
    
    Args:
        symbol: Símbolo da ação
        days: Número de dias para calcular estatísticas
    """
    try:
        symbol = symbol.upper()
        start_date = datetime.now() - timedelta(days=days)
        
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    COUNT(*) as count,
                    AVG(close) as avg_price,
                    MIN(low) as min_price,
                    MAX(high) as max_price,
                    AVG(volume) as avg_volume,
                    STDDEV(close) as volatility
                FROM stock_data
                WHERE symbol = :symbol
                AND time >= :start_date
            """)
            
            result = conn.execute(
                query,
                {'symbol': symbol, 'start_date': start_date}
            ).fetchone()
            
            if not result or result[0] == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data found for symbol {symbol}"
                )
            
            return {
                'symbol': symbol,
                'period_days': days,
                'data_points': result[0],
                'average_price': float(result[1]) if result[1] else None,
                'min_price': float(result[2]) if result[2] else None,
                'max_price': float(result[3]) if result[3] else None,
                'average_volume': int(result[4]) if result[4] else None,
                'volatility': float(result[5]) if result[5] else None
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/collect/scheduled")
async def scheduled_collection():
    """
    Endpoint para coleta agendada (pode ser chamado por cron job)
    Coleta dados das principais ações
    """
    try:
        # Ações principais para coleta diária
        popular_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
            'META', 'NVDA', 'JPM', 'V', 'WMT',
            'MA', 'UNH', 'HD', 'DIS', 'NFLX'
        ]
        
        collector = StockDataCollector()
        result = collector.collect_multiple_stocks(
            popular_stocks,
            period="5d",  # Últimos 5 dias
            interval="1d"
        )
        
        return {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "results": result
        }
        
    except Exception as e:
        logger.error(f"Error in scheduled collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)