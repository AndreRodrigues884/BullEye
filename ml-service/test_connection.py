import os
from sqlalchemy import create_engine, text

db_url = os.getenv('DATABASE_URL')
print(f'DATABASE_URL do container: {db_url}')

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT current_database(), current_user'))
        print(f'Conectado como: {result.fetchone()}')
        
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        tables = result.fetchall()
        print(f'Total de tabelas: {len(tables)}')
        for table in tables:
            print(f'  - {table[0]}')
except Exception as e:
    print(f'ERRO: {e}')