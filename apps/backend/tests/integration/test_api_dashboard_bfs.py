import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_bfs_api_dashboard_requires_auth_401(async_client: AsyncClient) -> None:
    r = await async_client.get("/api/v1/dashboard/stats")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_bfs_api_dashboard_returns_zero_stats_for_new_user(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    r = await async_client.get("/api/v1/dashboard/stats", headers=auth_headers)
    assert r.status_code == 200
    assert r.json() == {
        "total_items": 0,
        "active_warranties": 0,
        "expiring_soon": 0,
    }


@pytest.mark.asyncio
async def test_bfs_api_dashboard_counts_total_items(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    item_without_warranty,
    item_with_active_warranty,
) -> None:
    r = await async_client.get("/api/v1/dashboard/stats", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["total_items"] == 2


@pytest.mark.asyncio
async def test_bfs_api_dashboard_counts_only_active_warranties(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    item_with_active_warranty,
    item_with_expiring_warranty,
    item_with_expired_warranty,
) -> None:
    r = await async_client.get("/api/v1/dashboard/stats", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["active_warranties"] == 2


@pytest.mark.asyncio
async def test_bfs_api_dashboard_counts_only_expiring_soon_inside_window(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    item_with_active_warranty,
    item_with_expiring_warranty,
) -> None:
    r = await async_client.get("/api/v1/dashboard/stats", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["expiring_soon"] == 1


@pytest.mark.asyncio
async def test_bfs_api_dashboard_excludes_other_users_data(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
    item_without_warranty,
    other_user_item,
) -> None:
    r = await async_client.get("/api/v1/dashboard/stats", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["total_items"] == 1


@pytest.mark.asyncio
async def test_bfs_api_dashboard_response_shape(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    r = await async_client.get("/api/v1/dashboard/stats", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"total_items", "active_warranties", "expiring_soon"}
    assert isinstance(data["total_items"], int)
    assert isinstance(data["active_warranties"], int)
    assert isinstance(data["expiring_soon"], int)
