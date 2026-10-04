# Weatherline

A lightweight weather dashboard built with Streamlit and the OpenWeather API. Search a city for current conditions or a near-term forecast, with temperature, humidity, wind, and pressure in one view.

## Features

- Current conditions and a forecast selection for today or tomorrow
- Temperature, feels-like temperature, humidity, wind speed, and pressure
- Ten-minute caching for successful API responses
- Clear handling for missing credentials, unknown cities, and API/network errors
- Responsive Streamlit layout and a custom light theme

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- An API key from [OpenWeather](https://openweathermap.org/api)

## Run locally

1. Clone the repository and open its directory.
2. Create a local environment file from the example:

	```powershell
	Copy-Item .env.example .env
	```

3. Add your OpenWeather key to `.env`:

	```text
	OPENWEATHER_API_KEY=your_api_key
	```

4. Install the locked dependencies and launch the app:

	```powershell
	uv sync
	uv run streamlit run main.py
	```

Streamlit prints the local URL when the server starts, usually <http://localhost:8501>.

## Streamlit Community Cloud

Set the app secret in the deployment's **Settings > Secrets** panel:

```toml
OPENWEATHER_API_KEY = "your_api_key"
```

The local `.env` and `.streamlit/secrets.toml` files are excluded from Git. Never commit API keys.

## Quality checks

Run tests and static checks before opening a pull request:

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

GitHub Actions runs these checks on pushes and pull requests. Run `uv lock` after changing dependencies and commit the updated `uv.lock` to keep installs reproducible.

## Project layout

```text
.
├── .github/workflows/ci.yml
├── .streamlit/config.toml
├── main.py
├── pyproject.toml
├── tests/
└── uv.lock
```

## Data source

Weather observations and forecast data are provided by [OpenWeather](https://openweathermap.org/). Temperatures are displayed in Celsius, wind speed in metres per second, and pressure in hectopascals.
