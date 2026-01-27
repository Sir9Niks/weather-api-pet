# tests/schemas.py
# Схемы основаны на официальных примерах OpenWeatherMap (2024–2025)

CURRENT_WEATHER_SCHEMA = {
    "type": "object",
    "required": ["coord", "weather", "base", "main", "visibility", "wind", "clouds", "dt", "sys", "timezone", "id", "name", "cod"],
    "properties": {
        "coord": {
            "type": "object",
            "required": ["lon", "lat"],
            "properties": {
                "lon": {"type": "number"},
                "lat": {"type": "number"}
            }
        },
        "weather": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "main", "description", "icon"],
                "properties": {
                    "id": {"type": "integer"},
                    "main": {"type": "string"},
                    "description": {"type": "string"},
                    "icon": {"type": "string"}
                }
            }
        },
        "base": {"type": "string"},
        "main": {
            "type": "object",
            "required": ["temp", "feels_like", "temp_min", "temp_max", "pressure", "humidity"],
            "properties": {
                "temp": {"type": ["number", "integer"]},
                "feels_like": {"type": ["number", "integer"]},
                "temp_min": {"type": ["number", "integer"]},
                "temp_max": {"type": ["number", "integer"]},
                "pressure": {"type": "integer"},
                "humidity": {"type": "integer"},
                "sea_level": {"type": "integer", "default": None},
                "grnd_level": {"type": "integer", "default": None}
            }
        },
        "visibility": {"type": "integer"},
        "wind": {
            "type": "object",
            "required": ["speed", "deg"],
            "properties": {
                "speed": {"type": "number"},
                "deg": {"type": "integer"},
                "gust": {"type": "number", "default": None}
            }
        },
        "clouds": {
            "type": "object",
            "required": ["all"],
            "properties": {"all": {"type": "integer"}}
        },
        "dt": {"type": "integer"},
        "sys": {
            "type": "object",
            "required": ["country", "sunrise", "sunset"],
            "properties": {
                "type": {"type": "integer"},
                "id": {"type": "integer"},
                "country": {"type": "string"},
                "sunrise": {"type": "integer"},
                "sunset": {"type": "integer"}
            }
        },
        "timezone": {"type": "integer"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "cod": {"oneOf": [{"type": "integer"}, {"type": "string"}]}
    }
}

FORECAST_5DAY_SCHEMA = {
    "type": "object",
    "required": ["cod", "message", "cnt", "list", "city"],
    "properties": {
        "cod": {"type": "string"},
        "message": {"type": ["number", "integer"]},
        "cnt": {"type": "integer", "minimum": 1},
        "list": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["dt", "main", "weather", "clouds", "wind", "visibility", "pop", "sys", "dt_txt"],
                "properties": {
                    "dt": {"type": "integer"},
                    "main": {
                        "type": "object",
                        "required": ["temp", "feels_like", "temp_min", "temp_max", "pressure", "humidity", "temp_kf"],
                        "properties": {
                            "temp": {"type": ["number", "integer"]},
                            "feels_like": {"type": ["number", "integer"]},
                            "temp_min": {"type": ["number", "integer"]},
                            "temp_max": {"type": ["number", "integer"]},
                            "pressure": {"type": "integer"},
                            "sea_level": {"type": "integer"},
                            "grnd_level": {"type": "integer"},
                            "humidity": {"type": "integer"},
                            "temp_kf": {"type": ["number", "integer"]}
                        }
                    },
                    "weather": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["id", "main", "description", "icon"]
                        }
                    },
                    "clouds": {
                        "type": "object",
                        "required": ["all"]
                    },
                    "wind": {
                        "type": "object",
                        "required": ["speed", "deg"]
                    },
                    "visibility": {"type": "integer"},
                    "pop": {"type": "number"},
                    "rain": {
                        "type": "object",
                        "properties": {"3h": {"type": "number"}},
                        "default": {}
                    },
                    "snow": {
                        "type": "object",
                        "properties": {"3h": {"type": "number"}},
                        "default": {}
                    },
                    "sys": {
                        "type": "object",
                        "required": ["pod"],
                        "properties": {"pod": {"type": "string", "enum": ["d", "n"]}}
                    },
                    "dt_txt": {"type": "string"}
                }
            }
        },
        "city": {
            "type": "object",
            "required": ["id", "name", "coord", "country", "timezone", "sunrise", "sunset"],
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "coord": {
                    "type": "object",
                    "required": ["lat", "lon"]
                },
                "country": {"type": "string"},
                "population": {"type": "integer"},
                "timezone": {"type": "integer"},
                "sunrise": {"type": "integer"},
                "sunset": {"type": "integer"}
            }
        }
    }
}