"""
Перед імпортом app підставляємо DATABASE_* на тестову PostgreSQL БД.

URL за замовчуванням — для pytest *всередині* контейнера backend (db:5432).
З хоста задай TEST_DATABASE_URL на 127.0.0.1:5433 тощо.

БД `bfs_test`: `make test-backend` або CREATE DATABASE вручну.

DDL/TRUNCATE — синхронний psycopg2 (DATABASE_URL_SYNC).

Для httpx ASGITransport + asyncpg потрібен NullPool на async engine
(у pyproject один session event loop), інакше asyncpg:
«another operation is in progress».
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator
from datetime import date, timedelta
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import apply_pytest_database_environ, settings

apply_pytest_database_environ()
_async = settings.DATABASE_URL
_sync = settings.DATABASE_URL_SYNC

import app.db.session as session_mod  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.models.category import Category  # noqa: E402
from app.db.models.item import Item  # noqa: E402
from app.db.models.user import User  # noqa: E402
from app.db.models.warranty import Warranty  # noqa: E402
from app.main import app  # noqa: E402


async def _dispose_default_engine() -> None:
    await session_mod.engine.dispose()


asyncio.run(_dispose_default_engine())

session_mod.engine = create_async_engine(_async, poolclass=NullPool)
session_mod.AsyncSessionLocal = async_sessionmaker(
    session_mod.engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope="session")
def _sync_engine():
    eng = create_engine(_sync, pool_pre_ping=True)
    yield eng
    eng.dispose()


@pytest.fixture(scope="session", autouse=True)
def postgres_schema(_sync_engine) -> None:
    Base.metadata.drop_all(_sync_engine)
    Base.metadata.create_all(_sync_engine)


@pytest.fixture(autouse=True)
def clean_tables(_sync_engine) -> Any:
    with _sync_engine.begin() as conn:
        conn.execute(
            text(
                "TRUNCATE TABLE warranties, items, categories, users "
                "RESTART IDENTITY CASCADE"
            )
        )
    yield


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_mod.AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def auth_token(async_client: AsyncClient) -> str:
    register_resp = await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "secret1a",
        },
    )
    assert register_resp.status_code == 201
    return register_resp.json()["access_token"]


@pytest_asyncio.fixture
async def second_user_token(async_client: AsyncClient) -> str:
    resp = await async_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Second User",
            "email": "seconduser@example.com",
            "password": "secret1a",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers(auth_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {auth_token}"}


@pytest_asyncio.fixture
async def second_user_headers(second_user_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {second_user_token}"}


@pytest_asyncio.fixture
async def electronics_category(db_session: AsyncSession) -> Category:
    category = Category(name="Electronics")
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)
    return category


@pytest_asyncio.fixture
async def furniture_category(db_session: AsyncSession) -> Category:
    category = Category(name="Furniture")
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)
    return category


@pytest_asyncio.fixture
async def auth_user(
    db_session: AsyncSession,
    auth_token: str,
) -> User:
    result = await db_session.execute(
        text("SELECT id FROM users WHERE email=:email"),
        {"email": "testuser@example.com"},
    )
    row = result.first()
    assert row is not None

    user = await db_session.get(User, row.id)
    assert user is not None
    return user


@pytest_asyncio.fixture
async def second_user(
    db_session: AsyncSession,
    second_user_token: str,
) -> User:
    result = await db_session.execute(
        text("SELECT id FROM users WHERE email=:email"),
        {"email": "seconduser@example.com"},
    )
    row = result.first()
    assert row is not None

    user = await db_session.get(User, row.id)
    assert user is not None
    return user


@pytest_asyncio.fixture
async def item_without_warranty(
    db_session: AsyncSession,
    auth_user: User,
    electronics_category: Category,
) -> Item:
    item = Item(
        user_id=auth_user.id,
        name="Laptop",
        description="Work laptop",
        purchase_date=date.today() - timedelta(days=30),
        purchase_price=1500,
        category_id=electronics_category.id,
        photo_path=None,
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)
    return item


@pytest_asyncio.fixture
async def item_with_active_warranty(
    db_session: AsyncSession,
    auth_user: User,
    electronics_category: Category,
) -> Item:
    item = Item(
        user_id=auth_user.id,
        name="Phone",
        description="Smartphone",
        purchase_date=date.today() - timedelta(days=100),
        purchase_price=999,
        category_id=electronics_category.id,
        photo_path=None,
    )
    db_session.add(item)
    await db_session.flush()

    warranty = Warranty(
        item_id=item.id,
        provider="Apple Store",
        expiry_date=date.today() + timedelta(days=120),
        notes="Standard warranty",
    )
    db_session.add(warranty)
    await db_session.commit()
    await db_session.refresh(item)
    return item


@pytest_asyncio.fixture
async def item_with_expiring_warranty(
    db_session: AsyncSession,
    auth_user: User,
    furniture_category: Category,
) -> Item:
    item = Item(
        user_id=auth_user.id,
        name="Monitor",
        description="27 inch monitor",
        purchase_date=date.today() - timedelta(days=200),
        purchase_price=450,
        category_id=furniture_category.id,
        photo_path=None,
    )
    db_session.add(item)
    await db_session.flush()

    warranty = Warranty(
        item_id=item.id,
        provider="Dell",
        expiry_date=date.today() + timedelta(days=10),
        notes="Expiring soon",
    )
    db_session.add(warranty)
    await db_session.commit()
    await db_session.refresh(item)
    return item


@pytest_asyncio.fixture
async def item_with_expired_warranty(
    db_session: AsyncSession,
    auth_user: User,
    electronics_category: Category,
) -> Item:
    item = Item(
        user_id=auth_user.id,
        name="Old Tablet",
        description="Expired device",
        purchase_date=date.today() - timedelta(days=500),
        purchase_price=250,
        category_id=electronics_category.id,
        photo_path=None,
    )
    db_session.add(item)
    await db_session.flush()

    warranty = Warranty(
        item_id=item.id,
        provider="Samsung",
        expiry_date=date.today() - timedelta(days=5),
        notes="Expired warranty",
    )
    db_session.add(warranty)
    await db_session.commit()
    await db_session.refresh(item)
    return item


@pytest_asyncio.fixture
async def other_user_item(
    db_session: AsyncSession,
    second_user: User,
    electronics_category: Category,
) -> Item:
    item = Item(
        user_id=second_user.id,
        name="Other User Item",
        description="Should not be counted",
        purchase_date=date.today() - timedelta(days=20),
        purchase_price=111,
        category_id=electronics_category.id,
        photo_path=None,
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)
    return item


def make_payload(
    *,
    name: str = "Laptop",
    category_id: int | None = None,
    purchase_date: str | None = "2024-01-01",
    purchase_price: str | None = "1000.00",
    description: str | None = "Test item",
    warranty: dict[str, Any] | None = None,
) -> str:
    data: dict[str, Any] = {
        "name": name,
        "category_id": category_id,
        "purchase_date": purchase_date,
        "purchase_price": purchase_price,
        "description": description,
        "warranty": warranty,
    }
    return json.dumps(data)
