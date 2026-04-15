import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def auth_headers():
    unique = uuid.uuid4().hex[:8]
    payload = {
        "name": f"User {unique}",
        "email": f"user_{unique}@example.com",
        "password": "Password123",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_category_helper(headers, name="Test Category"):
    response = client.post(
        "/api/v1/categories",
        json={"name": name},
        headers=headers,
    )
    assert response.status_code == 200
    return response.json()


def test_get_categories():
    headers = auth_headers()
    response = client.get("/api/v1/categories", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_categories_returns_objects_with_required_fields():
    headers = auth_headers()
    create_category_helper(headers, "Check Fields")

    response = client.get("/api/v1/categories", headers=headers)
    data = response.json()

    assert len(data) > 0
    for category in data:
        assert "id" in category
        assert "name" in category


def test_create_category():
    headers = auth_headers()
    payload = {"name": "Kitchen"}

    response = client.post("/api/v1/categories", json=payload, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Kitchen"
    assert "id" in data


def test_create_category_persists_in_list():
    headers = auth_headers()
    created = create_category_helper(headers, "Persistent Category")

    response = client.get("/api/v1/categories", headers=headers)
    data = response.json()

    assert any(c["id"] == created["id"] for c in data)


def test_create_multiple_categories():
    headers = auth_headers()
    create_category_helper(headers, "Cat1")
    create_category_helper(headers, "Cat2")

    response = client.get("/api/v1/categories", headers=headers)
    data = response.json()

    names = [c["name"] for c in data]

    assert "Cat1" in names
    assert "Cat2" in names


def test_update_category():
    headers = auth_headers()
    created = create_category_helper(headers, "Old Name")

    response = client.put(
        f"/api/v1/categories/{created['id']}",
        json={"name": "New Name"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_update_category_persists():
    headers = auth_headers()
    created = create_category_helper(headers, "Before Update")

    client.put(
        f"/api/v1/categories/{created['id']}",
        json={"name": "After Update"},
        headers=headers,
    )

    response = client.get("/api/v1/categories", headers=headers)
    data = response.json()

    assert any(c["id"] == created["id"] and c["name"] == "After Update" for c in data)


def test_update_non_existing_category_returns_404():
    headers = auth_headers()

    response = client.put(
        "/api/v1/categories/999999",
        json={"name": "Does Not Exist"},
        headers=headers,
    )

    assert response.status_code == 404


def test_delete_category():
    headers = auth_headers()
    created = create_category_helper(headers, "Temp Category")

    response = client.delete(
        f"/api/v1/categories/{created['id']}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_deleted_category_not_in_list():
    headers = auth_headers()
    created = create_category_helper(headers, "To Delete")

    client.delete(f"/api/v1/categories/{created['id']}", headers=headers)

    response = client.get("/api/v1/categories", headers=headers)
    data = response.json()

    assert all(category["id"] != created["id"] for category in data)


def test_delete_non_existing_category_returns_404():
    headers = auth_headers()

    response = client.delete("/api/v1/categories/999999", headers=headers)

    assert response.status_code == 404


def test_create_category_missing_name_returns_422():
    headers = auth_headers()
    response = client.post("/api/v1/categories", json={}, headers=headers)

    assert response.status_code == 422


def test_update_category_missing_name_returns_422():
    headers = auth_headers()
    created = create_category_helper(headers, "Valid")

    response = client.put(
        f"/api/v1/categories/{created['id']}",
        json={},
        headers=headers,
    )

    assert response.status_code == 422


def test_create_category_empty_name():
    headers = auth_headers()
    response = client.post(
        "/api/v1/categories",
        json={"name": ""},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == ""


def test_category_ids_are_unique():
    headers = auth_headers()
    c1 = create_category_helper(headers, "Unique1")
    c2 = create_category_helper(headers, "Unique2")

    assert c1["id"] != c2["id"]
