import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

IMAGE_DIR = Path(__file__).resolve().parent / "images"
API_BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_api_key():
    api_key = os.getenv("OPENWEATHER_API_KEY") or os.getenv("api_key")
    if not api_key:
        try:
            api_key = st.secrets["OPENWEATHER_API_KEY"]
        except (KeyError, FileNotFoundError):
            api_key = None

    if not api_key:
        st.error("Set OPENWEATHER_API_KEY in your environment or Streamlit secrets.")
        st.stop()

    return api_key


def fetch_weather(endpoint, city):
    url = f"{API_BASE_URL}/{endpoint}"
    params = {
        "q": city,
        "appid": get_api_key(),
        "units": "metric",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as error:
        status_code = error.response.status_code if error.response else None
        if status_code == 404:
            st.error("City not found. Check the spelling and try again.")
        elif status_code == 401:
            st.error("The OpenWeather API key is invalid or not active.")
        else:
            st.error("The weather service returned an error. Please try again.")
    except (requests.RequestException, ValueError):
        st.error(
            "Could not retrieve weather data. Check your connection and try again."
        )

    return None


def get_weather(city):
    return fetch_weather("weather", city)


def get_forecast(city):
    data = fetch_weather("forecast", city)
    if data is None:
        return None

    forecast = data.get("list") if isinstance(data, dict) else None
    if not isinstance(forecast, list) or len(forecast) <= 8:
        st.error("Forecast data is unavailable for this city.")
        return None

    return forecast[8]


def display_temp(data):
    temp = f"{data['main']['temp']}°"
    max_temp = f"{data['main']['temp_max']}°"
    min_temp = f"{data['main']['temp_min']}°"

    col1, col2, col3, col4 = st.columns(4)

    with col2:
        st.metric(label="Maximum Temperature", value=max_temp)

    with col3:
        st.metric(label="Minimum Temperature", value=min_temp)

    with col4:
        st.metric(label="Average Temperature", value=temp)

    with col1:
        st.image(str(IMAGE_DIR / "temp_image.png"), width=100)


def display_wind(data):
    wind_speed = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]

    col1, col2, col3, col4 = st.columns(4)

    with col2:
        st.metric(label="Wind Speed", value=wind_speed)

    with col3:
        st.metric(label="Humidity", value=humidity)

    with col4:
        st.metric(label="Pressure", value=pressure)

    with col1:
        st.image(str(IMAGE_DIR / "wind_image.png"), width=100)


def interface(data):
    if data:
        description = str(data["weather"][0]["description"])
        feels_like = f"{data['main']['feels_like']}°"

        display_temp(data)

        st.info(f"{description.capitalize()} / Feels like : {feels_like}")

        display_wind(data)


def main():
    st.title("WEATHER APP")

    city = st.text_input("Enter the city name ").lower().strip()
    select = st.pills("Select", ["Today", "Tomorrow"], default="Today")

    if not city:
        st.info("Enter a city to see the weather.")
        return

    weather_data = get_weather(city) if select == "Today" else get_forecast(city)
    if weather_data:
        interface(weather_data)


if __name__ == "__main__":
    main()
