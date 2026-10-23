import requests
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Подключаем сценарии из feature-файла
scenarios("../features/petstore.feature")

# Заголовки для обхода базовых блокировок + Таймаут 10 секунд
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
TIMEOUT = 10  # Защита от бесконечного зависания

# ============================================================
# GIVEN шаги
# ============================================================

@given("базовый URL API настроен")
def base_url_configured(base_url):
    assert base_url.startswith("https://"), "URL должен быть валидным"

@given(parsers.parse('подготовлены данные для нового питомца с именем "{name}" и статусом "{status}"'))
def prepare_new_pet_payload(request_payload, name, status):
    request_payload["data"] = {
        "id": 12345,
        "name": name,
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": ["string"],
        "tags": [{"id": 1, "name": "tag1"}],
        "status": status
    }

@given(parsers.parse('подготовлены данные для обновления питомца с ID {pet_id:d} и именем "{name}"'))
def prepare_update_pet_payload(request_payload, pet_id, name):
    request_payload["data"] = {
        "id": pet_id,
        "name": name,
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": ["string"],
        "tags": [{"id": 1, "name": "tag1"}],
        "status": "available"
    }

@given(parsers.parse('подготовлены данные для нового заказа с petId {pet_id:d}'))
def prepare_order_payload(request_payload, pet_id):
    request_payload["data"] = {
        "id": 10,
        "petId": pet_id,
        "quantity": 1,
        "shipDate": "2026-10-23T10:00:00.000Z",
        "status": "placed",
        "complete": True
    }

@given(parsers.parse('подготовлены данные для нового пользователя с username "{username}"'))
def prepare_user_payload(request_payload, username):
    request_payload["data"] = {
        "id": 999,
        "username": username,
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }

@given("подготовлен массив данных для двух новых пользователей")
def prepare_users_array_payload(request_payload):
    request_payload["data"] = [
        {
            "id": 101,
            "username": "user_array_1",
            "firstName": "Alice",
            "lastName": "Smith",
            "email": "alice@example.com",
            "password": "password123",
            "phone": "1111111111",
            "userStatus": 1
        },
        {
            "id": 102,
            "username": "user_array_2",
            "firstName": "Bob",
            "lastName": "Jones",
            "email": "bob@example.com",
            "password": "password123",
            "phone": "2222222222",
            "userStatus": 1
        }
    ]

# ============================================================
# WHEN шаги
# ============================================================

@when(parsers.parse('выполняется GET запрос к "{endpoint}"'))
def send_get_request(base_url, endpoint, api_response):
    url = f"{base_url}{endpoint}"
    api_response["response"] = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

@when(parsers.parse('выполняется POST запрос к "{endpoint}" с этими данными'))
def send_post_request(base_url, endpoint, request_payload, api_response):
    url = f"{base_url}{endpoint}"
    api_response["response"] = requests.post(url, json=request_payload["data"], headers=HEADERS, timeout=TIMEOUT)

@when(parsers.parse('выполняется PUT запрос к "{endpoint}" с этими данными'))
def send_put_request(base_url, endpoint, request_payload, api_response):
    url = f"{base_url}{endpoint}"
    api_response["response"] = requests.put(url, json=request_payload["data"], headers=HEADERS, timeout=TIMEOUT)

@when(parsers.parse('выполняется DELETE запрос к "{endpoint}"'))
def send_delete_request(base_url, endpoint, api_response):
    url = f"{base_url}{endpoint}"
    api_response["response"] = requests.delete(url, headers=HEADERS, timeout=TIMEOUT)

# ============================================================
# THEN шаги
# ============================================================

@then(parsers.parse("статус-код ответа должен быть {expected_status:d}"))
def check_status_code(api_response, expected_status):
    response = api_response.get("response")
    assert response is not None, "Ответ от API не был получен"
    assert response.status_code == expected_status, (
        f"Ожидался статус-код {expected_status}, но получен {response.status_code}. "
        f"Тело ответа: {response.text}"
    )