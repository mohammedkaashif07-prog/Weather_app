import requests
import streamlit as st


def get_weather(city):
    api_key = "dedb55e45cc1a598eea144b3012e0ae9"
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Enter a valid city")
        st.stop()


def get_forecast(city):
    api_key = "dedb55e45cc1a598eea144b3012e0ae9"
    base_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    response = requests.get(base_url)

    try:
        data = response.json()
        return data
    except KeyError:
        st.error("Something went wrong.")


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
        st.image("images\\temp_image.png", width=100)


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
        st.image("images\\wind_image.png", width=100)


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

    weather_data = get_weather(city)
    forecast_data = get_forecast(city)["list"][8]

    select = st.pills("Select", ["Today", "Tomorrow"])

    if select == "Today":
        interface(weather_data)
    elif select == "Tomorrow":
        interface(forecast_data)


if __name__ == "__main__":
    main()
