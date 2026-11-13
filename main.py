import os
from dataclasses import dataclass
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


@dataclass
class WeatherReport:
    city: str
    condition: str
    temp_c: float
    humidity: int

    def summary(self) -> str:
        return (
            f"--- Weather Summary for {self.city} ---\n"
            f"Condition : {self.condition.capitalize()}\n"
            f"Temp      : {self.temp_c:.1f}°C\n"
            f"Humidity  : {self.humidity}%"
        )


def fetch_weather(city: str, api_key: str) -> WeatherReport:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  # Raises an HTTPError for 4xx/5xx responses
    data = response.json()

    return WeatherReport(
        city=data["name"],
        condition=data["weather"][0]["description"],
        temp_c=data["main"]["temp"],
        humidity=data["main"]["humidity"],
    )


if __name__ == "__main__":
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("WEATHER_API_KEY not found in .env file.")

    report = fetch_weather("Cairo", api_key)
    print(report.summary())