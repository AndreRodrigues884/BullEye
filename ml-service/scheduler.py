# ml-service/scheduler.py
# processo paralelo que agenda coletas (diárias, horárias, semanais).
import schedule
import time
import logging
from datetime import datetime
from data_collector import StockDataCollector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataCollectionScheduler:
    """Agendador para coleta automática de dados"""
    
    def __init__(self):
        self.collector = StockDataCollector()
        
        # Lista de ações para coleta regular
        self.watchlist = [
            # Tech Giants
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA',
            # Finance
            'JPM', 'BAC', 'WFC', 'GS', 'MS',
            # Consumer
            'WMT', 'COST', 'HD', 'NKE', 'MCD',
            # Healthcare
            'UNH', 'JNJ', 'PFE', 'ABBV', 'TMO',
            # Others
            'V', 'MA', 'DIS', 'NFLX', 'INTC'
        ]
        
    def daily_collection(self):
        """Coleta diária - dados do dia anterior"""
        try:
            logger.info("Starting daily collection...")
            result = self.collector.collect_multiple_stocks(
                self.watchlist,
                period="5d",  # Últimos 5 dias para garantir
                interval="1d"
            )
            logger.info(f"Daily collection completed: {result}")
        except Exception as e:
            logger.error(f"Error in daily collection: {str(e)}")
    
    def hourly_collection(self):
        """Coleta horária - para dados intraday"""
        try:
            logger.info("Starting hourly collection...")
            # Apenas algumas ações principais para coleta horária
            main_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
            
            result = self.collector.collect_multiple_stocks(
                main_stocks,
                period="1d",
                interval="1h"
            )
            logger.info(f"Hourly collection completed: {result}")
        except Exception as e:
            logger.error(f"Error in hourly collection: {str(e)}")
    
    def weekly_full_sync(self):
        """Sincronização semanal completa"""
        try:
            logger.info("Starting weekly full sync...")
            result = self.collector.collect_multiple_stocks(
                self.watchlist,
                period="1y",  # Último ano completo
                interval="1d"
            )
            logger.info(f"Weekly sync completed: {result}")
        except Exception as e:
            logger.error(f"Error in weekly sync: {str(e)}")
    
    def start(self):
        """Inicia o agendador"""
        logger.info("🎯 Starting BullEye Data Collection Scheduler...")
        
        # Agendar tarefas
        # Coleta diária às 18:00 (após fechamento do mercado US)
        schedule.every().day.at("18:00").do(self.daily_collection)
        
        # Coleta horária durante horário de mercado (9h às 16h)
        for hour in range(9, 17):
            schedule.every().day.at(f"{hour:02d}:00").do(self.hourly_collection)
        
        # Sincronização completa aos domingos às 00:00
        schedule.every().sunday.at("00:00").do(self.weekly_full_sync)
        
        # Executar primeira coleta imediatamente
        logger.info("Running initial collection...")
        self.daily_collection()
        
        # Loop principal
        logger.info("Scheduler started. Running tasks...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar a cada minuto


# Script de teste manual
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='BullEye Data Collection')
    parser.add_argument(
        '--mode',
        choices=['scheduler', 'manual', 'test'],
        default='test',
        help='Modo de execução'
    )
    parser.add_argument(
        '--symbols',
        nargs='+',
        help='Símbolos para coleta manual'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'scheduler':
        # Modo agendador
        scheduler = DataCollectionScheduler()
        scheduler.start()
        
    elif args.mode == 'manual':
        # Coleta manual
        if not args.symbols:
            print("❌ Por favor especifique símbolos: --symbols AAPL MSFT")
            exit(1)
            
        collector = StockDataCollector()
        result = collector.collect_multiple_stocks(
            args.symbols,
            period="1y",
            interval="1d"
        )
        print(f"\n✅ Coleta concluída: {result}")
        
    elif args.mode == 'test':
        # Teste rápido
        print("🧪 Modo teste - coletando 3 ações...")
        collector = StockDataCollector()
        result = collector.collect_multiple_stocks(
            ['AAPL', 'MSFT', 'GOOGL'],
            period="1mo",
            interval="1d"
        )
        print(f"\n✅ Teste concluído: {result}")


# ml-service/Dockerfile - Adicionar comando para scheduler
# CMD ["python", "scheduler.py", "--mode", "scheduler"]