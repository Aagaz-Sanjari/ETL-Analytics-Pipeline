# Crypto ETL & Analytics Pipeline

An end-to-end data pipeline that pulls live cryptocurrency prices, cleans and enriches the data, stores it in PostgreSQL, computes rolling analytics from accumulated history, and visualizes trends in Power BI.

## What it does

- **Extract**: Pulls live market data for 5 coins (Bitcoin, Ethereum, Solana, Cardano, Polkadot) from the CoinGecko API
- **Transform**: Cleans the raw data, handles missing values, and adds engineered features (e.g. flagging large 24h price movers)
- **Load**: Appends the processed data into a PostgreSQL database, building a historical record with every run
- **Analytics**: Reads the full accumulated history from PostgreSQL and computes a rolling moving average and volatility per coin
- **Visualization**: A Power BI dashboard connected directly to the database, showing price trends per coin

## Architecture

```
CoinGecko API
     |
     v
extract.py  -->  data/raw/*.json
     |
     v
transform.py  -->  data/processed/*.csv
     |
     v
load.py  -->  PostgreSQL (crypto_prices table)
     |
     v
compute_analytics.py  -->  rolling averages & volatility
     |
     v
Power BI Dashboard
```

## Tech stack

Python, Pandas, Requests, SQLAlchemy, PostgreSQL, Power BI

## Project structure

```
ETL-Analytics-Pipeline/
├── extract/
│   └── extract.py
├── transform/
│   └── transform.py
├── load/
│   └── load.py
├── sql/
│   └── analytics.sql
├── compute_analytics.py
├── crypto-analytics-dashboard.pbix
├── requirements.txt
└── .env (not committed — see setup below)
```

## Setup

1. Clone the repo and create a virtual environment:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your PostgreSQL credentials:
```
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_analytics
```

3. Create the database and table in PostgreSQL (see `sql/analytics.sql` for reference queries once data is loaded).

## Running the pipeline

```
python extract/extract.py
python transform/transform.py
python load/load.py
python compute_analytics.py
```

Each run pulls fresh prices and appends them to the database, building historical data over time. Running it repeatedly (or on a schedule) allows the rolling average and volatility calculations to become more meaningful.

## Sample output

After several runs, `compute_analytics.py` outputs each coin's latest price alongside its rolling average and volatility:

```
Loaded 35 historical rows across 5 coins

Latest rolling metrics per coin:
      id  current_price  moving_avg_price  rolling_volatility
polkadot       1.110000          1.110000            0.000000
 bitcoin   83216.000000      83237.000000           36.373067
 cardano       0.234165          0.234365            0.000347
ethereum    2635.830000       2637.153333            2.292081
  solana     113.010000        113.043333            0.057735
```

## Dashboard

The Power BI dashboard (`crypto-analytics-dashboard.pbix`) connects directly to the PostgreSQL database and displays price trends per coin over time.

## Future improvements

- Orchestrate the pipeline with Airflow instead of manual runs
- Add incremental extraction (only pull new data since the last run)
- Containerize with Docker for portable deployment
- Add automated data quality checks
