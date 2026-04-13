from io import BytesIO

import pytest
from httpx import AsyncClient

from tests.conftest import make_payload


@pytest.mark.asyncio
async def test_bfs_api_items_create_requires_auth_401(
    async_client: AsyncClient,
    electronics_category,
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        data={"payload": make_payload(category_id=electronics_category.id)},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_bfs_api_items_create_minimal_item_201(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    electronics_category,
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={"payload": make_payload(category_id=electronics_category.id)},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Laptop"
    assert data["warranty"] is None


@pytest.mark.asyncio
async def test_bfs_api_items_create_with_warranty_201(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    electronics_category,
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={
            "payload": make_payload(
                name="Phone",
                category_id=electronics_category.id,
                warranty={
                    "provider": "Apple Store",
                    "expiry_date": "2026-12-31",
                    "notes": "2 years",
                },
            )
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["warranty"] is not None
    assert data["warranty"]["provider"] == "Apple Store"


@pytest.mark.asyncio
async def test_bfs_api_items_create_invalid_payload_json_422(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={"payload": "{not-valid-json]"},
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_bfs_api_items_create_empty_name_422(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    electronics_category,
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={
            "payload": make_payload(
                name="",
                category_id=electronics_category.id,
            )
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_bfs_api_items_create_negative_price_422(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    electronics_category,
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={
            "payload": make_payload(
                category_id=electronics_category.id,
                purchase_price="-50.00",
            )
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_bfs_api_items_create_warranty_without_expiry_422(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    electronics_category,
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={
            "payload": make_payload(
                category_id=electronics_category.id,
                warranty={"provider": "Store", "notes": "Missing expiry"},
            )
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_bfs_api_items_create_unknown_category_404(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={"payload": make_payload(category_id=99999)},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Category not found"


@pytest.mark.asyncio
async def test_bfs_api_items_create_with_photo_persists_photo_path(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    electronics_category,
) -> None:
    r = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={"payload": make_payload(category_id=electronics_category.id)},
        files={"photo": ("camera.jpg", BytesIO(b"fake-image"), "image/jpeg")},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["photo_path"] is not None
    assert data["photo_path"].endswith(".jpg")


@pytest.mark.asyncio
async def test_bfs_api_items_create_updates_dashboard_counts(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    electronics_category,
) -> None:
    create_resp = await async_client.post(
        "/api/v1/items",
        headers=auth_headers,
        data={
            "payload": make_payload(
                category_id=electronics_category.id,
                warranty={
                    "provider": "Store",
                    "expiry_date": "2026-04-20",
                    "notes": "Within expiring window",
                },
            )
        },
    )
    assert create_resp.status_code == 201, create_resp.text

    stats_resp = await async_client.get(
        "/api/v1/dashboard/stats",
        headers=auth_headers,
    )
    assert stats_resp.status_code == 200, stats_resp.text

    stats = stats_resp.json()
    assert stats["total_items"] == 1
    assert stats["active_warranties"] == 1
    assert stats["expiring_soon"] == 1
