import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

def fetch_daily_prices(symbol: str) -> pd.DataFrame:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    ts = data.get("Time Series (Daily)", {})
    
    records = []
    for date, vals in ts.items():
        records.append({
            "date": date,
            "open": float(vals["1. open"]),
            "high": float(vals["2. high"]),
            "low": float(vals["3. low"]),
            "close": float(vals["4. close"]),
            "volume": int(vals["5. volume"]),
            "symbol": symbol,
            "fetched_at": datetime.utcnow(),
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)

if __name__ == "__main__":
    df = fetch_daily_prices("AAPL")
    print(df.tail())
    df.to_csv("data/raw/AAPL_daily.csv", index=False)
    print("Saved to data/raw/AAPL_daily.csv")