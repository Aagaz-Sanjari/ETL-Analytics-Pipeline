import requests

from connectors.base import Connector


class OpenMeteoCurrent(Connector):
    source = "open_meteo"
    dataset = "current"

    def fetch(self):
        records = []
        for city in self.params["cities"]:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
                    "timezone": "UTC",
                },
                timeout=15,
            )
            response.raise_for_status()
            current = response.json()["current"]
            records.append(
                {
                    "city": city["name"],
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "observed_at": current["time"],
                    "temperature_c": current["temperature_2m"],
                    "humidity_pct": current["relative_humidity_2m"],
                    "wind_speed_kmh": current["wind_speed_10m"],
                    "precipitation_mm": current["precipitation"],
                }
            )
        return records