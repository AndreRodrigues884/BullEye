# ml-service/db_utils.py
"""
Utilitários para trabalhar com a base de dados do BullEye
"""

from sqlalchemy import create_engine, text, inspect
import pandas as pd
import os
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()


class DatabaseUtils:
    """Ferramentas úteis para trabalhar com a BD"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self.engine = create_engine(self.db_url)
    
    def list_tables(self):
        """Lista todas as tabelas no banco"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        
        print("\n📊 Tabelas disponíveis:")
        print("=" * 50)
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print("=" * 50)
        return tables
    
    def describe_table(self, table_name: str):
        """Mostra estrutura de uma tabela"""
        inspector = inspect(self.engine)
        
        print(f"\n📋 Estrutura da tabela: {table_name}")
        print("=" * 80)
        
        # Colunas
        columns = inspector.get_columns(table_name)
        
        col_data = []
        for col in columns:
            col_data.append([
                col['name'],
                str(col['type']),
                'NULL' if col['nullable'] else 'NOT NULL',
                col.get('default', '')
            ])
        
        print(tabulate(
            col_data,
            headers=['Coluna', 'Tipo', 'Nullable', 'Default'],
            tablefmt='grid'
        ))
        
        # Índices
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("\n🔍 Índices:")
            for idx in indexes:
                print(f"  - {idx['name']}: {', '.join(idx['column_names'])}")
        
        # Chaves estrangeiras
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            print("\n🔗 Foreign Keys:")
            for fk in fks:
                print(f"  - {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
        
        print("=" * 80)
    
    def count_records(self, table_name: str):
        """Conta registros em uma tabela"""
        with self.engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).fetchone()
            count = result[0]
            print(f"\n📈 Total de registros em '{table_name}': {count:,}")
            return count
    
    def preview_table(self, table_name: str, limit: int = 10):
        """Mostra primeiros registros de uma tabela"""
        df = pd.read_sql(
            f"SELECT * FROM {table_name} LIMIT {limit}",
            self.engine
        )
        
        print(f"\n👀 Preview da tabela '{table_name}' (primeiros {limit} registros):")
        print("=" * 100)
        print(df.to_string())
        print("=" * 100)
        return df
    
    def get_stock_summary(self):
        """Resumo de dados de ações"""
        with self.engine.connect() as conn:
            # Total de símbolos
            total_symbols = conn.execute(
                text("SELECT COUNT(*) FROM stock_symbols")
            ).fetchone()[0]
            
            # Total de dados históricos
            total_data = conn.execute(
                text("SELECT COUNT(*) FROM stock_data")
            ).fetchone()[0]
            
            # Símbolos com dados
            symbols_with_data = conn.execute(
                text("SELECT COUNT(DISTINCT symbol) FROM stock_data")
            ).fetchone()[0]
            
            # Range de datas
            date_range = conn.execute(
                text("""
                    SELECT 
                        MIN(time) as oldest,
                        MAX(time) as newest,
                        MAX(time) - MIN(time) as range
                    FROM stock_data
                """)
            ).fetchone()
            
            print("\n" + "=" * 60)
            print("📊 RESUMO DA BASE DE DADOS - BullEye")
            print("=" * 60)
            print(f"Total de símbolos cadastrados: {total_symbols}")
            print(f"Símbolos com dados históricos: {symbols_with_data}")
            print(f"Total de registros históricos: {total_data:,}")
            
            if date_range and date_range[0]:
                print(f"\nRange de datas:")
                print(f"  Mais antiga: {date_range[0].strftime('%Y-%m-%d')}")
                print(f"  Mais recente: {date_range[1].strftime('%Y-%m-%d')}")
                print(f"  Período: {date_range[2].days} dias")
            
            print("=" * 60)
    
    def get_symbol_stats(self, symbol: str):
        """Estatísticas detalhadas de um símbolo"""
        with self.engine.connect() as conn:
            stats = conn.execute(
                text("""
                    SELECT 
                        COUNT(*) as total_records,
                        MIN(time) as first_date,
                        MAX(time) as last_date,
                        MIN(low) as min_price,
                        MAX(high) as max_price,
                        AVG(close) as avg_price,
                        AVG(volume) as avg_volume,
                        STDDEV(close) as price_volatility
                    FROM stock_data
                    WHERE symbol = :symbol
                """),
                {'symbol': symbol}
            ).fetchone()
            
            if not stats or stats[0] == 0:
                print(f"\n❌ Nenhum dado encontrado para {symbol}")
                return
            
            print("\n" + "=" * 60)
            print(f"📈 Estatísticas: {symbol}")
            print("=" * 60)
            print(f"Total de registros: {stats[0]:,}")
            print(f"Primeira data: {stats[1].strftime('%Y-%m-%d')}")
            print(f"Última data: {stats[2].strftime('%Y-%m-%d')}")
            print(f"\nPreços:")
            print(f"  Mínimo: ${stats[3]:.2f}")
            print(f"  Máximo: ${stats[4]:.2f}")
            print(f"  Média: ${stats[5]:.2f}")
            print(f"  Volatilidade: ${stats[7]:.2f}")
            print(f"\nVolume médio: {int(stats[6]):,}")
            print("=" * 60)
    
    def check_data_quality(self):
        """Verifica qualidade dos dados"""
        print("\n🔍 Verificando qualidade dos dados...")
        print("=" * 60)
        
        with self.engine.connect() as conn:
            # Verificar dados nulos
            null_check = conn.execute(
                text("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(*) FILTER (WHERE open IS NULL) as null_open,
                        COUNT(*) FILTER (WHERE close IS NULL) as null_close,
                        COUNT(*) FILTER (WHERE volume IS NULL) as null_volume
                    FROM stock_data
                """)
            ).fetchone()
            
            print(f"Total de registros: {null_check[0]:,}")
            print(f"Valores NULL:")
            print(f"  Open: {null_check[1]}")
            print(f"  Close: {null_check[2]}")
            print(f"  Volume: {null_check[3]}")
            
            # Verificar preços inválidos
            invalid_prices = conn.execute(
                text("""
                    SELECT COUNT(*) 
                    FROM stock_data
                    WHERE open <= 0 OR close <= 0 OR high < low
                """)
            ).fetchone()[0]
            
            print(f"\nPreços inválidos: {invalid_prices}")
            
            # Gaps nos dados
            gaps = conn.execute(
                text("""
                    SELECT symbol, COUNT(*) as gaps
                    FROM (
                        SELECT 
                            symbol,
                            time,
                            LAG(time) OVER (PARTITION BY symbol ORDER BY time) as prev_time,
                            time - LAG(time) OVER (PARTITION BY symbol ORDER BY time) as gap
                        FROM stock_data
                    ) t
                    WHERE gap > INTERVAL '5 days'
                    GROUP BY symbol
                    ORDER BY gaps DESC
                    LIMIT 5
                """)
            ).fetchall()
            
            if gaps:
                print("\n⚠️  Símbolos com gaps significativos (>5 dias):")
                for symbol, gap_count in gaps:
                    print(f"  {symbol}: {gap_count} gaps")
            
        print("=" * 60)
    
    def reset_table(self, table_name: str):
        """CUIDADO: Apaga todos os dados de uma tabela"""
        confirm = input(f"\n⚠️  TEM CERTEZA que quer apagar '{table_name}'? (yes/no): ")
        if confirm.lower() == 'yes':
            with self.engine.connect() as conn:
                conn.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))
                conn.commit()
            print(f"✅ Tabela '{table_name}' limpa!")
        else:
            print("❌ Operação cancelada")


# Script interativo
if __name__ == "__main__":
    import sys
    
    db = DatabaseUtils()
    
    if len(sys.argv) < 2:
        print("\n🎯 BullEye Database Utils")
        print("\nUso:")
        print("  python db_utils.py list              - Listar tabelas")
        print("  python db_utils.py describe TABLE    - Descrever tabela")
        print("  python db_utils.py count TABLE       - Contar registros")
        print("  python db_utils.py preview TABLE     - Preview da tabela")
        print("  python db_utils.py summary           - Resumo geral")
        print("  python db_utils.py stats SYMBOL      - Estatísticas de um símbolo")
        print("  python db_utils.py quality           - Verificar qualidade")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'list':
        db.list_tables()
    
    elif command == 'describe' and len(sys.argv) > 2:
        db.describe_table(sys.argv[2])
    
    elif command == 'count' and len(sys.argv) > 2:
        db.count_records(sys.argv[2])
    
    elif command == 'preview' and len(sys.argv) > 2:
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        db.preview_table(sys.argv[2], limit)
    
    elif command == 'summary':
        db.get_stock_summary()
    
    elif command == 'stats' and len(sys.argv) > 2:
        db.get_symbol_stats(sys.argv[2].upper())
    
    elif command == 'quality':
        db.check_data_quality()
    
    else:
        print("❌ Comando inválido ou faltam argumentos")