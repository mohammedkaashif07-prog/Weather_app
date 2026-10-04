from pathlib import Path

import pytest
import requests
from streamlit.testing.v1 import AppTest

import main


def test_http_error_includes_provider_reason_without_request_url():
    response = requests.Response()
    response.status_code = 400
    response.url = "https://api.openweathermap.org/?appid=secret"
    response._content = b'{"message":"invalid city query"}'
    error = requests.HTTPError(response=response)

    message = main.describe_http_error(error)

    assert message == "Weather service error (HTTP 400): invalid city query"
    assert "secret" not in message


@pytest.mark.parametrize(
    ("forecast_day", "expected"),
    [("Today", "current"), ("Tomorrow", "forecast")],
)
def test_weather_selection_routes_to_expected_endpoint(
    monkeypatch, forecast_day, expected
):
    requested = []

    def get_weather(city):
        requested.append(("current", city))
        return "current"

    def get_forecast(city):
        requested.append(("forecast", city))
        return "forecast"

    monkeypatch.setattr(main, "get_weather", get_weather)
    monkeypatch.setattr(main, "get_forecast", get_forecast)

    result = main.get_weather_for_day("Oslo", forecast_day)

    assert result == expected
    assert requested == [(expected, "Oslo")]


def test_home_page_renders_without_credentials_or_api_calls():
    app_path = Path(__file__).parents[1] / "main.py"
    app = AppTest.from_file(str(app_path)).run()

    assert not app.exception
    assert app.title[0].value == "Weatherline"
    assert app.info[0].value == "Search for a city to see its local forecast."
