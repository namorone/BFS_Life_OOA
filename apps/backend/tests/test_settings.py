from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_settings():
    response = client.get("/api/v1/settings")

    assert response.status_code == 200

    data = response.json()
    assert "full_name" in data
    assert "email" in data
    assert "notifications_enabled" in data
    assert "warranty_reminders_enabled" in data
    assert "preferred_currency" in data


def test_update_settings():
    payload = {
        "full_name": "Oleksandr Zhenchenko",
        "email": "oleksandr@gmail.com",
        "notifications_enabled": False,
        "warranty_reminders_enabled": True,
        "preferred_currency": "EUR",
    }

    response = client.put("/api/v1/settings", json=payload)

    assert response.status_code == 200
    assert response.json() == payload
