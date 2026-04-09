import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_engine():
    DB_HOST = os.getenv("DB_HOST", "localhost")
    url = f"postgresql://postgres:{DB_PASSWORD}@{DB_HOST}:5432/alphasignal"
    engine = create_engine(url)
    return engine
def load_prices(df: pd.DataFrame):
    engine = get_engine()
    df.to_sql("stock_prices", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into stock_prices table")

if __name__ == "__main__":
    from fetch_prices import fetch_daily_prices
    df = fetch_daily_prices("AAPL")
    load_prices(df)