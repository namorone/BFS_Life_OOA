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
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import apply_pytest_database_environ, settings  # noqa: E402

# До інших import app.*: тестова БД, далі ті самі поля, що в Settings.
apply_pytest_database_environ()
_async = settings.DATABASE_URL
_sync = settings.DATABASE_URL_SYNC

import app.db.session as session_mod  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.models import Category, Item, User, Warranty  # noqa: E402, F401
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
