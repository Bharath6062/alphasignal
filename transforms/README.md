# AlphaSignal — Automated Stock Data Pipeline

A production-grade data engineering pipeline that ingests, transforms, and serves live equity market data.

## Architecture
```
Alpha Vantage API → Python Ingestion → PostgreSQL → dbt Transformations → FastAPI
```

## Tech Stack

- **Python** — data ingestion and pipeline orchestration
- **PostgreSQL** — relational database for raw and transformed data
- **SQLAlchemy** — Python to PostgreSQL connector
- **dbt** — SQL transformation layer
- **FastAPI** — REST API to serve data
- **schedule** — automated daily pipeline execution

## Pipeline Components

- `src/ingestion/fetch_prices.py` — fetches daily stock prices from Alpha Vantage API
- `src/ingestion/db_loader.py` — loads price data into PostgreSQL using SQLAlchemy
- `transforms/models/stock_metrics.sql` — dbt model calculating daily return, price range, and 7-day moving average
- `src/api/main.py` — FastAPI endpoints serving raw prices and calculated metrics
- `src/pipeline.py` — automated scheduler with error handling and logging

## API Endpoints

- `GET /prices/{symbol}` — returns raw daily price data for a stock
- `GET /metrics/{symbol}` — returns transformed financial metrics

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add your credentials to `.env`:
```
ALPHA_VANTAGE_KEY=your_key
DB_PASSWORD=your_password
```