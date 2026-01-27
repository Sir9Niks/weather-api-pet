import pytest
import requests
import time
from jsonschema import validate, ValidationError
from schemas import CURRENT_WEATHER_SCHEMA

@pytest.mark.parametrize("city", ["Amsterdam", "London", "Berlin", "Moscow"])
def test_get_current_weather_success(city, weather_url, api_key):
    """Позитивный тест: получение текущей погоды"""
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "en"
    }

    start_time = time.time()
    response = requests.get(weather_url, params=params, timeout=10)
    response_time_ms = (time.time() - start_time) * 1000

    # Основные assertions
    assert response.status_code == 200
    data = response.json()

    try:
        validate(instance=data, schema=CURRENT_WEATHER_SCHEMA)
    except ValidationError as ve:
        pytest.fail(f"Current weather JSON Schema validation failed: {ve.message}")

    assert data["cod"] == 200
    assert data["name"] == city
    assert "main" in data
    assert "weather" in data and len(data["weather"]) > 0

    temp = data["main"]["temp"]
    assert isinstance(temp, (int, float))
    assert -60 < temp < 60   # разумный диапазон

    assert "wind" in data
    assert response_time_ms < 4000   # < 4 секунды


def test_invalid_city_not_found(weather_url, api_key):
    """Негативный тест: город не существует"""
    params = {
        "q": "NonExistentCityXYZ12345",
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(weather_url, params=params)

    assert response.status_code == 404
    data = response.json()
    assert data["cod"] == "404"
    assert "city not found" in data["message"].lower()


# Дополнительно: можно добавить тест с units=imperial