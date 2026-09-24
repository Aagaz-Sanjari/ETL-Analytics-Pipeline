import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

ROLLING_WINDOW = 3


def get_engine():
    connection_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_url)


def load_history(engine):
    query = """
        SELECT id, symbol, current_price, price_change_percentage_24h, pulled_at
        FROM crypto_prices
        ORDER BY id, pulled_at
    """
    df = pd.read_sql(query, engine)
    df["pulled_at"] = pd.to_datetime(df["pulled_at"])
    return df


def compute_rolling_metrics(df, window):
    df = df.sort_values(["id", "pulled_at"]).copy()

    df["moving_avg_price"] = (
        df.groupby("id")["current_price"]
        .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
    )

    df["rolling_volatility"] = (
        df.groupby("id")["current_price"]
        .transform(lambda x: x.rolling(window=window, min_periods=1).std())
    )

    df["rolling_volatility"] = df["rolling_volatility"].fillna(0)

    return df


def main():
    engine = get_engine()
    df = load_history(engine)

    print(f"Loaded {len(df)} historical rows across {df['id'].nunique()} coins")

    df = compute_rolling_metrics(df, ROLLING_WINDOW)

    latest = df.sort_values("pulled_at").groupby("id").tail(1)

    print("\nLatest rolling metrics per coin:")
    print(
        latest[["id", "current_price", "moving_avg_price", "rolling_volatility"]]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()