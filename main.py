import yfinance as yf
import os
import psycopg2 as pg
import pandas as pd
from dotenv import load_dotenv
from config import TICKERS, PPERIOD, INTERVAL
from contextlib import closing

class Data:
    def __init__(self, banco):
        self.db = banco
        
    def importData(self,ticker):
        try:
            df = yf.download(ticker, period=PPERIOD, interval=INTERVAL, progress=False)
            df_json = df.to_json(orient='records', date_format='iso')
            return df_json  
        except Exception as e:
            print(e)
            return None
    
    def salvar_ativos(self):
        for ticker in TICKERS:
            ativos_json = self.importData(ticker)
            if json_value := ativos_json:
                self.db.inserir_dados(ticker, json_value)
            
class Banco:
    def __init__(self):
        load_dotenv('vault.env')
        self.db_host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')            
        self.database = os.getenv('DB_NAME')            
        self.user = os.getenv('DB_USER')            
        self.db_key = os.getenv('DB_PASSWORD')            
    def conexao (self):
        conexao = pg.connect(
        database=self.database,
        user=self.user,
        password=self.db_key,
        host=self.db_host,
        port=self.port
        )
        return conexao
    
    def criar_tabela(self):
        with closing(self.conexao()) as conection:
            with conection.cursor() as cursor:
                cursor.execute("""                            
                    CREATE TABLE IF NOT EXISTS raw_acoes (
                        ticker VARCHAR(10) NOT NULL UNIQUE,
                        dados_API JSONB,
                        ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                    );
                """)        
                conection.commit() 
    def inserir_dados(self, ticker, dados_api):
        with self.conexao() as conection:
            with conection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO raw_acoes (ticker, dados_API)
                    VALUES (%s, %s)
                    ON CONFLICT (ticker)
                    DO NOTHING;
                """, (ticker, dados_api))
                conection.commit()
db = Banco()
dt = Data(db)        

db.criar_tabela()
dt.salvar_ativos()
