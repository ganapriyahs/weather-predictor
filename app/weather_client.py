import requests
from typing import Optional, Dict, Any

class WeatherClient:
    def __init__(self):
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    def get_coordinates(self, city_name: str) -> Optional[Dict[str, float]]:
        """
        Fetches latitude and longitude for a given city name.
        """
        params = {
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        try:
            response = requests.get(self.geocoding_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("results"):
                return None
                
            # Take the first result
            location = data["results"][0]
            return {
                "lat": location["latitude"],
                "lon": location["longitude"],
                "name": location["name"],
                "country": location.get("country")
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching coordinates: {e}")
            return None

    def get_current_weather(self, latitude: float, longitude: float):
        """
        Fetches current weather data for a given location.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "timezone": "auto"
        }
        
        try:
            response = requests.get(self.weather_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            return {
                "timestamp": current.get("time"),
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "wind_speed": current.get("wind_speed_10m"),
                "location_coords": {"lat": latitude, "lon": longitude}
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None