import pytest
import requests
import time
from jsonschema import validate, ValidationError
from schemas import FORECAST_5DAY_SCHEMA


@pytest.mark.parametrize("city, expected_cnt", [
    ("Amsterdam", 40),
    ("London", 40),
    ("Berlin", 40),
    ("Tokyo", 40),
])
def test_get_5day_forecast_success(city, expected_cnt, forecast_url, api_key):
    """Позитивный тест 5-day / 3-hour forecast + проверка схемы"""
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "en"
    }

    start = time.perf_counter()
    resp = requests.get(forecast_url, params=params, timeout=12)
    duration_ms = (time.perf_counter() - start) * 1000

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    data = resp.json()

    assert data["cod"] == "200"
    assert data["cnt"] == expected_cnt, f"Ожидалось {expected_cnt} точек, получено {data['cnt']}"
    assert len(data["list"]) == data["cnt"]
    assert data["city"]["name"].lower() in city.lower()   # иногда с регионом

    # Валидация полной структуры
    try:
        validate(instance=data, schema=FORECAST_5DAY_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Forecast schema validation failed:\n{e.message}\nPath: {list(e.path)}")

    assert duration_ms < 6000, f"Ответ слишком долгий: {duration_ms:.0f} мс"


@pytest.mark.parametrize("invalid_input, expected_code", [
    ({"q": "NonExistentCityXYZ987"}, 404),
    ({"q": ""}, 400),                     # пустой город
    ({"lat": 999, "lon": 999}, 400),      # некорректные координаты
])
def test_forecast_negative_cases(invalid_input, expected_code, forecast_url, api_key):
    """Негативные сценарии для /forecast"""
    params = {**invalid_input, "appid": api_key, "units": "metric"}
    resp = requests.get(forecast_url, params=params)

    assert resp.status_code == expected_code

    try:
        data = resp.json()
        assert str(data["cod"]) == str(expected_code)
        assert "message" in data
    except Exception as e:
        pytest.fail(f"Ожидался JSON с cod и message, но получено: {resp.text}")


def test_forecast_invalid_api_key(forecast_url):
    """Проверка на 401 при неверном ключе"""
    params = {"q": "Amsterdam", "appid": "fake-key-0000000000", "units": "metric"}
    resp = requests.get(forecast_url, params=params)

    assert resp.status_code == 401
    data = resp.json()
    assert data.get("cod") in (401, "401")
    assert "unauthorized" in str(data.get("message", "")).lower() or "invalid" in str(data.get("message", "")).lower()