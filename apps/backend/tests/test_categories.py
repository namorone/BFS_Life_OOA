from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_categories():
    response = client.get("/api/v1/categories")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_category():
    payload = {"name": "Kitchen"}

    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Kitchen"
    assert "id" in data


def test_update_category():
    create_response = client.post("/api/v1/categories", json={"name": "Old Name"})
    category_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/categories/{category_id}",
        json={"name": "New Name"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_category():
    create_response = client.post("/api/v1/categories", json={"name": "Temp Category"})
    category_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/categories/{category_id}")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_deleted_category_not_in_list():
    create_response = client.post("/api/v1/categories", json={"name": "To Delete"})
    category_id = create_response.json()["id"]

    client.delete(f"/api/v1/categories/{category_id}")

    response = client.get("/api/v1/categories")
    data = response.json()

    assert all(category["id"] != category_id for category in data)
