# Weather API Tests (OpenWeatherMap)

**PET-проект для демонстрации навыков автоматизированного тестирования REST API**

![PyTest](https://img.shields.io/badge/PyTest-8.0+-blue)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenWeatherMap](https://img.shields.io/badge/API-OpenWeatherMap-orange)

## О проекте

Этот проект — пример автоматизированного тестирования публичного REST API с использованием **PyTest**.  
Цель — показать навыки QA Automation Engineer:

- Написание позитивных и негативных тестов
- Параметризация тестов
- Валидация структуры ответа по **JSON Schema**
- Измерение времени ответа (производительность)
- Работа с фикстурами и конфигурацией (.env)
- Генерация красивых HTML-отчётов

**Тестируемые эндпоинты OpenWeatherMap (бесплатный уровень):**
- `/data/2.5/weather` — текущая погода по городу
- `/data/2.5/forecast` — 5-дневный прогноз (3-часовые интервалы)

**Что проверяют тесты:**
- Позитивные сценарии: получение корректных данных для реальных городов (Amsterdam, London, Berlin, Moscow, Tokyo и др.)
- Негативные сценарии: несуществующий город, пустой запрос, некорректные координаты, неверный API-ключ
- Полная валидация структуры JSON-ответов (jsonschema)
- Производительность: время ответа не превышает лимиты (4–6 секунд)
- Обработка ошибок и таймаутов

## Технологии

- **Python** 3.10+
- **PyTest** 8.0+
- **Requests**
- **jsonschema** — валидация структуры
- **python-dotenv** — работа с .env
- **pytest-html** — красивые HTML-отчёты

## Структура проекта


```
weather_api_pet/
├── logs/ # логи ошибок
├── tests/
    ├── conftest.py       # фикстуры (API-ключ, базовые URL)
    ├── schemas.py        # JSON-схемы для валидации
    ├── test_current_weather.py  # тесты текущей погоды
    └── test_forecast_weather.py # тесты 5-дневного прогноза
├── .env                  # Ваш API-ключ 
├── .env.example
├── .gitignore
├── openapi.yaml          # Swagger-документация API
├── README.md
├── report.html
├── requirements.txt
```
## Как запустить проект

### 1. Клонирование и установка

```bash
git clone https://github.com/Sir9Niks/weather-api-pet.git
cd weather-api-pet
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
# или
venv\Scripts\activate         # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка API-ключа

1. Зарегистрируйтесь на https://openweathermap.org/api и получите бесплатный API-ключ.
2. Скопируйте файл `.env.example` → `.env`
3. Вставьте ваш ключ:

```env
OPENWEATHER_API_KEY=ваш_ключ_сюда
```

## Запуск тестов

### Все тесты сразу (рекомендуется)

```bash
pytest -v --html=report.html --self-contained-html
```

- `-v` — подробный вывод
- `--html=report.html` — создаст красивый HTML-отчёт (откройте в браузере)

### Запуск тестов по отдельности

**Только тесты текущей погоды:**

```bash
pytest tests/test_current_weather.py -v
```

**Только тесты 5-дневного прогноза:**

```bash
pytest tests/test_forecast_weather.py -v
```

**Только позитивные тесты прогноза (с параметризацией):**

```bash
pytest tests/test_forecast_weather.py::test_get_5day_forecast_success -v
```

**Только негативные тесты прогноза:**

```bash
pytest tests/test_forecast_weather.py::test_forecast_negative_cases -v
```

**Только тест валидации схемы прогноза:**

```bash
pytest tests/test_forecast_weather.py::test_get_5day_forecast_success -v
```

## Что проверяют тесты

| Группа тестов                       | Что именно проверяется                                                                 |
|-------------------------------------|----------------------------------------------------------------------------------------|
| Текущая погода (test_current_weather.py) | Позитивные запросы по городам, негативные (несуществующий город, неверный ключ, пустой запрос), валидация схемы, время ответа < 4 сек |
| 5-дневный прогноз (test_forecast_weather.py) | Позитивные запросы (с параметризацией, с cnt=10), негативные сценарии, полная валидация схемы, время ответа < 6 сек |
| Общие проверки                      | Поведение при неверном API-ключе, обработка таймаутов, корректные ошибки 400/401/404 |

## Генерация отчёта

После запуска тестов откройте в браузере файл `report.html` — там будет красивая таблица со всеми тестами, статусами, временем выполнения и логами ошибок.

## Автор

**Андрей**  
QA Automation Engineer (портфолио-проект)  
2026
