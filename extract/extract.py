"""
extract.py
----------
Pulls daily market data for a basket of coins from the CoinGecko API
and saves the raw response to /data/raw as a timestamped JSON file.

CoinGecko free API needs no key: https://www.coingecko.com/en/api/documentation
"""

import requests
import json
import os
from datetime import datetime, timezone

# ---- Config ----
COINS = ["bitcoin", "ethereum", "solana", "cardano", "polkadot"]
VS_CURRENCY = "usd"
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_market_data(coins: list[str], vs_currency: str = "usd") -> list[dict]:
    """Call CoinGecko's /coins/markets endpoint for the given coin ids."""
    params = {
        "vs_currency": vs_currency,
        "ids": ",".join(coins),
        "order": "market_cap_desc",
        "price_change_percentage": "24h",
    }

    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()  # raises if the API call failed
    return response.json()


def save_raw_data(data: list[dict], directory: str) -> str:
    """Save the raw API response as a timestamped JSON file. Returns the file path."""
    os.makedirs(directory, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"prices_{timestamp}.json"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return filepath


def main():
    print(f"Fetching data for: {', '.join(COINS)}")
    data = fetch_market_data(COINS, VS_CURRENCY)

    filepath = save_raw_data(data, RAW_DATA_DIR)
    print(f"Saved {len(data)} records to {filepath}")

    # Quick sanity check printed to console
    for coin in data:
        print(f"  {coin['id']:<10} ${coin['current_price']:>10}  "
              f"24h change: {coin['price_change_percentage_24h']}%")


if __name__ == "__main__":
    main()