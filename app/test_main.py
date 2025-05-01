"""Tests for project"""
from datetime import datetime
from fastapi.testclient import TestClient
import pytest
from .main import app

client = TestClient(app)


# Фикстуры для тестовых данных
@pytest.fixture
def test_user():
    """Генерируем уникальное имя пользователя для каждого теста"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return {
        "user_name": f"testuser_{timestamp}",
        "user_full_name": "Test User",
        "user_bearer_access_token": f"token_{timestamp}"
    }


@pytest.fixture
def test_book():
    """Тестовые данные для метода /books"""
    return {
        "book_title": "Test Book",
        "book_author": "Test Author",
        "book_year": 2023
    }


# Тестовые сценарии
def test_create_user(test_user):
    """Тест создания пользователя /users"""
    response = client.post("/users", json=test_user)
    assert response.status_code == 201
    assert response.json()["message"] == "Пользователь успешно добавлен"


def test_create_book(test_user, test_book):
    """Тест создания книги /books"""
    # 1. Создаем уникального пользователя
    user_response = client.post("/users", json=test_user)
    assert user_response.status_code == 201

    # 2. Авторизуемся с токеном пользователя
    headers = {"Authorization": f"Bearer {test_user['user_bearer_access_token']}"}

    # 3. Создаем книгу
    book_response = client.post("/books", json=test_book, headers=headers)
    assert book_response.status_code == 201
    assert book_response.json()["message"] == "Книга успешно добавлена"


def test_book_flow(test_user, test_book):
    """
    Полный тест:
    1. Создаем пользователя
    2. Создаем книгу
    3. Создаем бронь
    """
    # 1. Создаем пользователя
    user_response = client.post("/users", json=test_user)
    assert user_response.status_code == 201, "Ошибка при создании пользователя"
    user_data = user_response.json()
    user_id = user_data["users"]["user_id"]

    # 2. Авторизуемся с токеном пользователя
    headers = {
        "Authorization": f"Bearer {test_user['user_bearer_access_token']}"
    }

    # 3. Создаем книгу
    book_response = client.post("/books", json=test_book, headers=headers)
    assert book_response.status_code == 201, "Ошибка при создании книги"
    book_data = book_response.json()
    assert "book" in book_data, "Ответ не содержит данных о книге"
    book_id = book_data["book"]["id"]

    # 4. Бронируем книгу
    booking_data = {"book_id": book_id, "user_id": user_id}
    booking_response = client.post(
        "/booking/issue",
        json=booking_data,
        headers=headers
    )
    assert booking_response.status_code == 201, "Ошибка при бронировании"
    booking_data = booking_response.json()
    assert "id" in booking_data, "Ответ не содержит ID бронирования"

def test_unauthorized_access():
    """Тест неавторизованного доступа к книгам /books"""
    response = client.get("/books")
    assert response.status_code == 403
    assert "Not authenticated" in response.json()["detail"]

def test_book_not_found(test_user):
    """Тест запроса несуществующей книги(несуществующего ID книги"""
    # 1. Создаем уникального пользователя
    user_response = client.post("/users", json=test_user)
    assert user_response.status_code == 201
    # 2. Авторизуемся с токеном пользователя
    headers = {"Authorization": f"Bearer {test_user['user_bearer_access_token']}"}
    # 3. Запрашиваем несуществующую книгу
    response = client.get("/books/999", headers=headers)
    assert response.status_code == 404
    assert "Книга с id 999 не найдена" in response.json()["detail"]
