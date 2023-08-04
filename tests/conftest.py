"""Конфигурация для тестирования."""
import uuid

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import make_url, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.database import get_async_session
from app.main import app
from app.models.base import Base
from app.settings import settings


@pytest.fixture
def test_db_name():
    test_db_name = f"{uuid.uuid4().hex}_pytest"
    return test_db_name


async def create_database(test_db_name):
    url = make_url(settings.DATABASE_URL)
    url = url.set(database="postgres")
    template_engine = create_async_engine(url, echo=False)

    async with template_engine.begin() as conn:
        await conn.execute(text("ROLLBACK"))
        await conn.execute(text(f'CREATE DATABASE "{test_db_name}";'))
        await conn.commit()
        await conn.close()
        await template_engine.dispose()


@pytest.fixture
async def sa_engine_db_async(test_db_name):
    await create_database(test_db_name)

    url = make_url(settings.DATABASE_URL)
    url = url.set(database=test_db_name)
    a_engine = create_async_engine(
        url, poolclass=NullPool, connect_args={"server_settings": {"jit": "off"}}
    )

    async with a_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield a_engine
    finally:
        async with a_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await a_engine.dispose()


@pytest.fixture
async def db(sa_engine_db_async):
    async_session = sessionmaker(
        sa_engine_db_async,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


@pytest.fixture
async def patch_sessionmaker(db, monkeypatch) -> None:
    def call(*args, **kwargs) -> AsyncSession:
        """Патч вызова sessionmaker.__call__(), который происходит в async_session(), in_transaction"""
        return db

    monkeypatch.setattr(sessionmaker, "__call__", call)


@pytest.fixture
async def api_client(patch_sessionmaker) -> AsyncClient:
    async with AsyncClient(app=app, base_url=f"https://test") as async_client:
        yield async_client
