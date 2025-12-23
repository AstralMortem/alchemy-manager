from pathlib import Path
from alchemy_manager import init_sync_db, init_async_db, Model
from alchemy_manager.session import sync_engine, async_engine
import pytest
import pytest_asyncio


@pytest.fixture(scope="session", autouse=True)
def setup_sync_db():
    db_path = Path("./sync_db.db")
    init_sync_db(f"sqlite:///{db_path}")

    with sync_engine() as engine:
        Model.metadata.create_all(engine)

    yield

    with sync_engine() as engine:
        Model.metadata.drop_all(engine)
        engine.engine.dispose()

    if db_path.exists():
        db_path.unlink()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_async_db():
    db_path = Path("./async_db.db")
    init_async_db(f"sqlite+aiosqlite:///{db_path}")

    async with async_engine() as conn:
        await conn.run_sync(Model.metadata.create_all)

    yield

    async with async_engine() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        conn.sync_engine.dispose()

    if db_path.exists():
        db_path.unlink()
