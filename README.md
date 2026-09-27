# Weather App

A Streamlit app that displays current weather and a short-term forecast using OpenWeatherMap.

## Setup

Add your OpenWeather API key to a `.env` file in the project directory:

```text
OPENWEATHER_API_KEY=your_api_key
```

Install dependencies and start the app:

```powershell
uv sync
uv run streamlit run main.py
```

For Streamlit Cloud, add `OPENWEATHER_API_KEY` to the app's secrets.
