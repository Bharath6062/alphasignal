import os
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
def get_engine():
    url= f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/alphasignal"
    engine = create_engine(url)
    return engine
app = FastAPI()
engine = get_engine ()

@app.get("/prices/{symbol}")
def get_prices(symbol: str):
    df = pd.read_sql(f"SELECT * FROM stock_prices WHERE symbol = '{symbol}'", engine)
    return df.to_dict(orient="records")

@app.get("/metrics/{symbol}")
def get_metrics(symbol: str):
    df = pd.read_sql(f"SELECT * FROM transforms.stock_metrics WHERE symbol = '{symbol}'", engine)
    return df.to_dict(orient="records")