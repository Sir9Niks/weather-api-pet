import pytest
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Папка для логов
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def api_key():
    """Фикстура для API-ключа. Проваливает сессию, если ключа нет."""
    if not API_KEY:
        pytest.fail("OPENWEATHER_API_KEY не задан в .env файле!")
    return API_KEY


@pytest.fixture
def weather_url():
    return f"{BASE_URL}/weather"


@pytest.fixture
def forecast_url():
    return f"{BASE_URL}/forecast"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук, который сохраняет подробный лог при ЛЮБОМ провале теста
    (включая ошибки в фикстурах setup, call и teardown).
    """
    outcome = yield
    rep = outcome.get_result()

    # Логируем любой failed-репорт
    if rep.failed:
        test_name = item.name
        test_nodeid = item.nodeid.replace("::", "_").replace("/", "_").replace(":", "")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"{LOG_DIR}/FAIL_{test_nodeid}_{timestamp}.log"

        with open(log_filename, "w", encoding="utf-8") as f:
            f.write(f"Тест: {test_name}\n")
            f.write(f"Полный nodeid: {item.nodeid}\n")
            f.write(f"Этап выполнения: {rep.when} (setup/call/teardown)\n")
            f.write(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Статус: FAILED\n")
            f.write("=" * 80 + "\n\n")

            # Параметры теста (если параметризация)
            if hasattr(item, "callspec") and item.callspec.params:
                f.write("Параметры теста:\n")
                for k, v in item.callspec.params.items():
                    f.write(f"  {k}: {v}\n")
                f.write("-" * 80 + "\n\n")

            # Traceback ошибки
            f.write("Traceback:\n")
            if rep.longrepr:
                f.write(str(rep.longrepr))
            else:
                f.write("Нет детального traceback (возможно, простое pytest.fail)\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("Конец лога\n")

        logger.info(f"Провал теста '{test_name}' на этапе {rep.when} — лог сохранён: {log_filename}")
