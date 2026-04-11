import asyncio

import pytest

from app import create_app
from app import database
from app.models import ModelBase


@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / "test.db"
    database_url = f"sqlite+aiosqlite:///{db_path.as_posix()}"

    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "DATABASE_URL": database_url,
        }
    )

    async def prepare_db() -> None:
        async with database.get_engine().begin() as conn:
            await conn.run_sync(ModelBase.metadata.create_all)

    async def cleanup_db() -> None:
        async with database.get_engine().begin() as conn:
            await conn.run_sync(ModelBase.metadata.drop_all)
        await database.dispose_db()

    asyncio.run(prepare_db())
    yield app
    asyncio.run(cleanup_db())


@pytest.fixture
def client(app):
    return app.test_client()
