import requests
from dataclasses import dataclass
import os


API_KEY = os.getenv("API_KEY")
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct?q="
DEFAULT_WEATHER_PARAMS = f"&appid={API_KEY}&mode=json&units=imperial&lang=en"
DEFAULT_GEOCODE_PARAMS = f"appid={API_KEY}"


@dataclass
class GeoCode:
    lat: float
    lon: float
    city: str
    state: str | None
    country: str | None


def get_location() -> None:
    city = input("City: ")
    state_code = input("State Code, only applicable to the USA: ")
    country_code = input("Country Code (2 letters): ")
    return f"{city},{state_code},{country_code}"


def get_geocode(location_payload):
    geocode_url = f"{BASE_GEOCODE_URL}{location_payload}&{DEFAULT_GEOCODE_PARAMS}"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()[0]
    lat = geocode_data["lat"]
    lon = geocode_data["lon"]
    country = geocode_data["country"]
    state = geocode_data["state"]
    city = geocode_data["name"]
    return GeoCode(
        lat,
        lon,
        city,
        state,
        country,
    )


# Use lat lon to obtain Current Weather
def get_weather(geocode: GeoCode):
    lat_long_payload = f"?lat={geocode.lat}&lon={geocode.lon}"
    weather_api_url = f"{BASE_WEATHER_URL}{lat_long_payload}{DEFAULT_WEATHER_PARAMS}"
    weather_response = requests.get(weather_api_url)
    weather_data = weather_response.json()
    temp = weather_data["main"]["temp"]
    condition = weather_data["weather"][0]["description"]
    return temp, condition


if __name__ == "__main__":
    print("Hi there!!\n")
    print(
        "Welcome to OpenWeatherPy. Plese enter the following location information. Only City is required. Just press <Enter> if you do not have the information:"
    )
    location_payload = get_location()
    geocode = get_geocode(location_payload)
    temp, condition = get_weather(geocode)
    print(
        f"The temperature in {geocode.city}, {geocode.state} is {temp} F with {condition}."
    )
