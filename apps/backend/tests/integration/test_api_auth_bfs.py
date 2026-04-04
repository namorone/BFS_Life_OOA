"""
API / інтеграція: login, register, JWT (твій фронтовий флоу).
Захищений GET лише як перевірка Bearer — без сценаріїв dashboard / items.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_bfs_api_auth_register_returns_token_and_user_for_login_flow(
    async_client: AsyncClient,
) -> None:
    r = await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "newuser@example.com",
            "password": "secret1a",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert "access_token" in data
    assert len(data["access_token"]) > 20
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["full_name"] == "Test User"


@pytest.mark.asyncio
async def test_bfs_api_auth_register_password_without_digit_422_like_register_page(
    async_client: AsyncClient,
) -> None:
    r = await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Weak",
            "email": "weak@example.com",
            "password": "onlyLetters",
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_bfs_api_auth_register_password_too_short_422(
    async_client: AsyncClient,
) -> None:
    r = await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "S",
            "email": "shortpw@example.com",
            "password": "a1",
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_bfs_api_auth_register_invalid_email_422(
    async_client: AsyncClient,
) -> None:
    r = await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "E",
            "email": "not-an-email",
            "password": "secret1a",
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_bfs_api_auth_register_duplicate_email_409(
    async_client: AsyncClient,
) -> None:
    body = {"name": "A", "email": "dup@example.com", "password": "secret1a"}
    r1 = await async_client.post("/api/v1/auth/register", json=body)
    assert r1.status_code == 201
    r2 = await async_client.post("/api/v1/auth/register", json=body)
    assert r2.status_code == 409


@pytest.mark.asyncio
async def test_bfs_api_auth_login_success_matching_login_page(
    async_client: AsyncClient,
) -> None:
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "myPass1a",
        },
    )
    r = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "myPass1a"},
    )
    assert r.status_code == 200
    assert r.json()["user"]["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_bfs_api_auth_login_email_case_insensitive_after_register(
    async_client: AsyncClient,
) -> None:
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Case",
            "email": "CaseMail@Example.com",
            "password": "secret1a",
        },
    )
    r = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "casemail@example.com", "password": "secret1a"},
    )
    assert r.status_code == 200
    assert r.json()["user"]["email"] == "casemail@example.com"


@pytest.mark.asyncio
async def test_bfs_api_auth_login_wrong_password_401(
    async_client: AsyncClient,
) -> None:
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "X",
            "email": "wrongpw@example.com",
            "password": "right1a",
        },
    )
    r = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "wrongpw@example.com", "password": "other1a"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_bfs_api_auth_login_unknown_email_401(
    async_client: AsyncClient,
) -> None:
    r = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "any1pass"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_bfs_api_auth_login_empty_password_422(
    async_client: AsyncClient,
) -> None:
    r = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "a@b.co", "password": ""},
    )
    assert r.status_code == 422


# Будь-який маршрут з get_current_user — лише перевірка JWT, не бізнес-логіка UI.
_PROTECTED = "/api/v1/categories"


@pytest.mark.asyncio
async def test_bfs_api_jwt_missing_bearer_401_on_protected_route(
    async_client: AsyncClient,
) -> None:
    r = await async_client.get(_PROTECTED)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_bfs_api_jwt_garbage_bearer_401_on_protected_route(
    async_client: AsyncClient,
) -> None:
    r = await async_client.get(
        _PROTECTED,
        headers={"Authorization": "Bearer not-a-real-jwt"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_bfs_api_jwt_valid_token_ok_on_protected_route(
    async_client: AsyncClient,
) -> None:
    await async_client.post(
        "/api/v1/auth/register",
        json={"name": "T", "email": "tok@example.com", "password": "secret1a"},
    )
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "tok@example.com", "password": "secret1a"},
    )
    token = login.json()["access_token"]
    r = await async_client.get(
        _PROTECTED,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
