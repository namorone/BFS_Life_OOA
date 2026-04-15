import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_settings():
    original = client.get("/api/v1/settings").json()
    yield
    client.put("/api/v1/settings", json=original)


def test_get_settings():
    response = client.get("/api/v1/settings")

    assert response.status_code == 200

    data = response.json()
    assert "full_name" in data
    assert "email" in data
    assert "notifications_enabled" in data
    assert "warranty_reminders_enabled" in data
    assert "preferred_currency" in data


def test_get_settings_response_shape():
    response = client.get("/api/v1/settings")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["full_name"], str)
    assert isinstance(data["email"], str)
    assert isinstance(data["notifications_enabled"], bool)
    assert isinstance(data["warranty_reminders_enabled"], bool)
    assert isinstance(data["preferred_currency"], str)


def test_update_settings():
    payload = {
        "full_name": "Roman Borovets",
        "email": "roman.borovets@gmail.com",
        "notifications_enabled": False,
        "warranty_reminders_enabled": True,
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 200
    assert response.json() == payload


def test_update_settings_persists_after_get():
    payload = {
        "full_name": "Roman Borovets",
        "email": "roman@gmail.com",
        "notifications_enabled": True,
        "warranty_reminders_enabled": False,
        "preferred_currency": "USD",
    }

    put_response = client.put("/api/v1/settings", json=payload)
    get_response = client.get("/api/v1/settings")

    assert put_response.status_code == 200
    assert get_response.status_code == 200
    assert get_response.json() == payload


def test_update_settings_can_disable_both_switches():
    payload = {
        "full_name": "Test User",
        "email": "test@gmail.com",
        "notifications_enabled": False,
        "warranty_reminders_enabled": False,
        "preferred_currency": "UAH",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["notifications_enabled"] is False
    assert data["warranty_reminders_enabled"] is False


def test_update_settings_can_enable_both_switches():
    payload = {
        "full_name": "Test User",
        "email": "test@gmail.com",
        "notifications_enabled": True,
        "warranty_reminders_enabled": True,
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["notifications_enabled"] is True
    assert data["warranty_reminders_enabled"] is True


@pytest.mark.parametrize("currency", ["USD", "EUR", "UAH"])
def test_update_settings_with_supported_currency(currency):
    payload = {
        "full_name": "Currency User",
        "email": "currency@gmail.com",
        "notifications_enabled": True,
        "warranty_reminders_enabled": True,
        "preferred_currency": currency,
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 200
    assert response.json()["preferred_currency"] == currency


def test_update_settings_missing_full_name_returns_422():
    payload = {
        "email": "test@gmail.com",
        "notifications_enabled": True,
        "warranty_reminders_enabled": True,
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 422


def test_update_settings_missing_email_returns_422():
    payload = {
        "full_name": "Test User",
        "notifications_enabled": True,
        "warranty_reminders_enabled": True,
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 422


def test_update_settings_missing_notifications_enabled_returns_422():
    payload = {
        "full_name": "Test User",
        "email": "test@gmail.com",
        "warranty_reminders_enabled": True,
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 422


def test_update_settings_missing_warranty_reminders_enabled_returns_422():
    payload = {
        "full_name": "Test User",
        "email": "test@gmail.com",
        "notifications_enabled": True,
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 422


def test_update_settings_missing_preferred_currency_returns_422():
    payload = {
        "full_name": "Test User",
        "email": "test@gmail.com",
        "notifications_enabled": True,
        "warranty_reminders_enabled": True,
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 422


def test_update_settings_invalid_notifications_enabled_type_returns_422():
    payload = {
        "full_name": "Test User",
        "email": "test@gmail.com",
        "notifications_enabled": "not-a-bool",
        "warranty_reminders_enabled": True,
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 422


def test_update_settings_invalid_warranty_reminders_enabled_type_returns_422():
    payload = {
        "full_name": "Test User",
        "email": "test@gmail.com",
        "notifications_enabled": True,
        "warranty_reminders_enabled": "not-a-bool",
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 422


def test_update_settings_accepts_empty_full_name_if_backend_allows_it():
    payload = {
        "full_name": "",
        "email": "emptyname@gmail.com",
        "notifications_enabled": True,
        "warranty_reminders_enabled": True,
        "preferred_currency": "USD",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 200
    assert response.json()["full_name"] == ""
