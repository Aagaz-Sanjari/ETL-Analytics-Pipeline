"""
load.py
-------
Loads the latest processed CSV file into PostgreSQL.
"""

import os
import glob
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROCESSED_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "processed"
)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def load_latest_csv(directory: str) -> pd.DataFrame:
    """Find and load the latest processed CSV file."""

    files = glob.glob(
        os.path.join(directory, "processed_*.csv")
    )

    if not files:
        raise FileNotFoundError(
            "No processed CSV files found. Run transform.py first."
        )

    latest_file = max(files, key=os.path.getctime)

    print(f"Loading: {latest_file}")

    return pd.read_csv(latest_file)


def load_to_postgres(df: pd.DataFrame):
    """Load DataFrame into PostgreSQL."""

    connection_url = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(connection_url)

    df.to_sql(
        "crypto_prices",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} rows into PostgreSQL.")


def main():

    df = load_latest_csv(PROCESSED_DATA_DIR)

    load_to_postgres(df)


if __name__ == "__main__":
    main()