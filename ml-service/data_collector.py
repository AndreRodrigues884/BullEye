# ml-service/data_collector.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockDataCollector:
    """Coleta dados de ações do Yahoo Finance"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self.engine = create_engine(self.db_url)
        
    def fetch_stock_data(
        self, 
        symbol: str, 
        period: str = "1y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Busca dados históricos de uma ação
        
        Args:
            symbol: Símbolo da ação (ex: AAPL, MSFT)
            period: Período de dados (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Intervalo (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
        Returns:
            DataFrame com dados históricos
        """
        try:
            import time
            logger.info(f"Fetching data for {symbol}...")
            
            # Headers para evitar bloqueio
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Delay para evitar rate limit
            time.sleep(2)
            
            ticker = yf.Ticker(symbol)
            
            # Buscar dados históricos
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            # Adicionar símbolo ao DataFrame
            df['symbol'] = symbol
            
            # Resetar index para ter time como coluna
            df.reset_index(inplace=True)
            
            # Renomear colunas para minúsculas
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            
            # Garantir que temos a coluna 'date' ou 'datetime'
            if 'date' in df.columns:
                df.rename(columns={'date': 'time'}, inplace=True)
            elif 'datetime' in df.columns:
                df.rename(columns={'datetime': 'time'}, inplace=True)
            
            logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def fetch_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        Busca informações gerais sobre a ação
        
        Args:
            symbol: Símbolo da ação
            
        Returns:
            Dicionário com informações da ação
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'exchange': info.get('exchange', 'Unknown'),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap'),
                'currency': info.get('currency', 'USD')
            }
            
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {str(e)}")
            return None
    
    def save_to_database(self, df: pd.DataFrame, table: str = 'stock_data'):
        """
        Salva dados no banco de dados
        
        Args:
            df: DataFrame com dados
            table: Nome da tabela
        """
        try:
            # Preparar dados para inserção
            df_to_save = df[[
                'time', 'symbol', 'open', 'high', 
                'low', 'close', 'volume'
            ]].copy()
            
            # Converter time para timestamp
            df_to_save['time'] = pd.to_datetime(df_to_save['time'])
            
            # Inserir dados (substituir duplicados)
            with self.engine.connect() as conn:
                # Deletar dados existentes para esse símbolo e período
                symbol = df_to_save['symbol'].iloc[0]
                min_date = df_to_save['time'].min()
                max_date = df_to_save['time'].max()
                
                delete_query = text("""
                    DELETE FROM stock_data 
                    WHERE symbol = :symbol 
                    AND time BETWEEN :min_date AND :max_date
                """)
                
                conn.execute(
                    delete_query,
                    {
                        'symbol': symbol,
                        'min_date': min_date,
                        'max_date': max_date
                    }
                )
                conn.commit()
            
            # Inserir novos dados
            df_to_save.to_sql(
                table,
                self.engine,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
            
            logger.info(f"Saved {len(df_to_save)} records to database")
            
        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
            raise
    
    def save_stock_info(self, info: Dict):
        """Salva informações da ação no banco"""
        try:
            with self.engine.connect() as conn:
                # Verificar se já existe
                check_query = text(
                    "SELECT id FROM stock_symbols WHERE symbol = :symbol"
                )
                result = conn.execute(
                    check_query, 
                    {'symbol': info['symbol']}
                ).fetchone()
                
                if result:
                    # Atualizar
                    update_query = text("""
                        UPDATE stock_symbols 
                        SET name = :name, 
                            exchange = :exchange, 
                            sector = :sector
                        WHERE symbol = :symbol
                    """)
                    conn.execute(update_query, info)
                else:
                    # Inserir
                    insert_query = text("""
                        INSERT INTO stock_symbols (symbol, name, exchange, sector)
                        VALUES (:symbol, :name, :exchange, :sector)
                    """)
                    conn.execute(insert_query, info)
                
                conn.commit()
                logger.info(f"Saved info for {info['symbol']}")
                
        except Exception as e:
            logger.error(f"Error saving stock info: {str(e)}")
    
    def collect_multiple_stocks(
        self, 
        symbols: List[str], 
        period: str = "1y",
        interval: str = "1d"
    ):
        """
        Coleta dados de múltiplas ações
        
        Args:
            symbols: Lista de símbolos
            period: Período de dados
            interval: Intervalo
        """
        logger.info(f"Starting collection for {len(symbols)} stocks...")
        
        success_count = 0
        error_count = 0
        
        for symbol in symbols:
            try:
                # Buscar e salvar dados históricos
                df = self.fetch_stock_data(symbol, period, interval)
                if df is not None:
                    self.save_to_database(df)
                    success_count += 1
                
                # Buscar e salvar informações da ação
                info = self.fetch_stock_info(symbol)
                if info:
                    self.save_stock_info(info)
                    
            except Exception as e:
                logger.error(f"Error processing {symbol}: {str(e)}")
                error_count += 1
                continue
        
        logger.info(
            f"Collection completed: {success_count} successful, "
            f"{error_count} errors"
        )
        
        return {
            'success': success_count,
            'errors': error_count,
            'total': len(symbols)
        }


# Função de teste
if __name__ == "__main__":
    collector = StockDataCollector()
    
    # Lista de ações populares para testar
    test_symbols = [
        'AAPL',  # Apple
        'MSFT',  # Microsoft
        'GOOGL', # Google
        'AMZN',  # Amazon
        'TSLA',  # Tesla
        'META',  # Meta
        'NVDA',  # Nvidia
        'JPM',   # JP Morgan
        'V',     # Visa
        'WMT'    # Walmart
    ]
    
    # Coletar dados dos últimos 2 anos
    result = collector.collect_multiple_stocks(
        test_symbols,
        period="2y",
        interval="1d"
    )
    
    print(f"\n✅ Collection completed!")
    print(f"Success: {result['success']}/{result['total']}")
    print(f"Errors: {result['errors']}")