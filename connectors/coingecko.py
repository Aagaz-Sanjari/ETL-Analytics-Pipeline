import requests

from connectors.base import Connector


class CoinGeckoMarkets(Connector):
    source = "coingecko"
    dataset = "markets"

    def fetch(self):
        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": self.params.get("vs_currency", "usd"),
                "ids": ",".join(self.params["coins"]),
                "order": "market_cap_desc",
                "price_change_percentage": "24h",
            },
            timeout=15,
        )
        response.raise_for_status()
        return response.json()