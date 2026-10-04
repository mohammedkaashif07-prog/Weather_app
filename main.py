import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://api.openweathermap.org/data/2.5"
WEATHER_ICON_URL = "https://openweathermap.org/img/wn/{icon}@4x.png"

st.set_page_config(
    page_title="Weatherline | Local forecast",
    page_icon=":material/wb_sunny:",
    layout="centered",
)


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


@st.cache_data(ttl=600, max_entries=128, show_spinner=False)
def _request_weather(endpoint, city, api_key):
    url = f"{API_BASE_URL}/{endpoint}"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_weather(endpoint, city):
    try:
        return _request_weather(endpoint, city, get_api_key())
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


def get_weather_for_day(city, forecast_day):
    if forecast_day == "Today":
        return get_weather(city)
    return get_forecast(city)


def display_weather(data):
    condition = data.get("weather", [{}])[0]
    measurements = data.get("main", {})
    city = data.get("name", "Selected location")
    country = data.get("sys", {}).get("country")
    location = f"{city}, {country}" if country else city

    st.subheader(location)
    description = str(condition.get("description", "Conditions unavailable"))
    st.caption(description.capitalize())

    with st.container(border=True):
        summary, icon_column = st.columns([3, 1], vertical_alignment="center")
        with summary:
            st.metric(
                "Temperature",
                f"{measurements.get('temp', '--')} °C",
                delta=f"Feels like {measurements.get('feels_like', '--')} °C",
            )
        with icon_column:
            icon = condition.get("icon")
            if icon:
                st.image(
                    WEATHER_ICON_URL.format(icon=icon),
                    width=104,
                    caption="Current conditions",
                )

    st.subheader("Conditions")
    wind_speed = data.get("wind", {}).get("speed", "--")
    columns = st.columns(3)
    columns[0].metric("Humidity", f"{measurements.get('humidity', '--')}%")
    columns[1].metric("Wind", f"{wind_speed} m/s")
    columns[2].metric("Pressure", f"{measurements.get('pressure', '--')} hPa")


def main():
    st.title("Weatherline", icon=":material/wb_sunny:")
    st.caption("A clear view of the weather where you are or where you're headed.")

    with st.form("weather_search"):
        city_column, forecast_column, submit_column = st.columns(
            [2.2, 1.2, 0.8], vertical_alignment="bottom"
        )
        with city_column:
            city = st.text_input("City", placeholder="e.g. Copenhagen")
        with forecast_column:
            forecast_day = st.segmented_control(
                "Forecast",
                ["Today", "Tomorrow"],
                default="Today",
                label_visibility="visible",
            )
        with submit_column:
            submitted = st.form_submit_button(
                "Search", type="primary", icon=":material/search:"
            )

    if not submitted:
        st.info(
            "Search for a city to see its local forecast.",
            icon=":material/location_on:",
        )
        return

    city = city.strip()
    if not city:
        st.warning("Enter a city name to continue.", icon=":material/edit_location:")
        return

    with st.spinner(f"Checking the forecast for {city}..."):
        weather_data = get_weather_for_day(city, forecast_day)
    if weather_data is not None:
        display_weather(weather_data)
        st.caption("Weather data provided by OpenWeather.")


if __name__ == "__main__":
    main()
