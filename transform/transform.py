"""
transform.py
------------
Reads the most recent raw JSON file from /data/raw, cleans it,
adds engineered features, and saves a processed CSV to /data/processed.
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime, timezone

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def load_latest_raw_file(directory: str) -> pd.DataFrame:
    """Find the most recently saved raw JSON file and load it into a DataFrame."""
    files = glob.glob(os.path.join(directory, "prices_*.json"))
    if not files:
        raise FileNotFoundError("No raw price files found. Run extract.py first.")

    latest_file = max(files, key=os.path.getctime)
    print(f"Loading: {latest_file}")

    df = pd.read_json(latest_file)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only the columns we need and handle missing values."""
    keep_cols = [
        "id", "symbol", "current_price", "market_cap",
        "total_volume", "price_change_percentage_24h", "last_updated"
    ]
    df = df[keep_cols].copy()

    # Drop rows with no price at all — can't do anything useful with those
    df = df.dropna(subset=["current_price"])

    # Fill missing 24h change with 0 rather than dropping the row
    df["price_change_percentage_24h"] = df["price_change_percentage_24h"].fillna(0)

    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["pulled_at"] = datetime.now(timezone.utc)

    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add simple engineered features based on this single pull.
    (Moving averages/volatility need multiple days of history —
    we'll compute those once we've accumulated more data over time.)
    """
    # Simple volatility proxy from the 24h change (real rolling volatility comes later)
    df["abs_24h_change"] = df["price_change_percentage_24h"].abs()

    # Flag big movers — a feature that's actually interesting to look at
    df["big_mover_flag"] = df["abs_24h_change"] > 5

    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic data quality checks — flag and drop clearly bad rows."""
    before = len(df)

    df = df[df["current_price"] > 0]
    df = df[df["market_cap"] >= 0]

    dropped = before - len(df)
    if dropped > 0:
        print(f"Validation: dropped {dropped} bad row(s)")

    return df


def save_processed_data(df: pd.DataFrame, directory: str) -> str:
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filepath = os.path.join(directory, f"processed_{timestamp}.csv")
    df.to_csv(filepath, index=False)
    return filepath


def main():
    df = load_latest_raw_file(RAW_DATA_DIR)
    df = clean_data(df)
    df = add_features(df)
    df = validate_data(df)

    filepath = save_processed_data(df, PROCESSED_DATA_DIR)
    print(f"Saved {len(df)} processed rows to {filepath}")
    print(df[["id", "current_price", "price_change_percentage_24h", "big_mover_flag"]])


if __name__ == "__main__":
    main()