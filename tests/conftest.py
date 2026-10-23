import pytest
import requests

# ✅ ИСПРАВЛЕНО: используем уникальное имя аргумента
def pytest_addoption(parser):
    parser.addoption(
        "--petstore-url",
        action="store",
        default="https://petstore.swagger.io/v2",
        help="Базовый URL для API Petstore"
    )

@pytest.fixture(scope="session")
def base_url(request):
    """Фикстура для получения базового URL из командной строки."""
    return request.config.getoption("--petstore-url")

@pytest.fixture
def api_response():
    """Фикстура для хранения ответа от API между шагами."""
    return {}

@pytest.fixture
def request_payload():
    """Фикстура для хранения тела запроса между шагами."""
    return {}