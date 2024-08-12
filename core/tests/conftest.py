import json
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi import UploadFile
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from core.database import Base, async_session_maker, engine, env
from core.main import app as fastapi_app
from core.models.files_models import Files


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert env("MODE") == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"core/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    files = open_mock_json("files")

    async with async_session_maker() as session:
        insert_users = insert(Files).values(files)
        await session.execute(insert_users)
        await session.commit()


@pytest.fixture
def mock_file():
    return AsyncMock(spec=UploadFile, filename="test.txt", size=1024)


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac
