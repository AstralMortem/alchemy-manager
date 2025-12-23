from contextlib import asynccontextmanager, contextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from contextvars import ContextVar

_sync_engine = ContextVar[Engine | None]("sync_engine", default=None)
_async_engine = ContextVar[AsyncEngine | None]("async_engine", default=None)


def init_sync_db(url: str, **kwargs):
    engine = create_engine(url, pool_pre_ping=True, **kwargs)
    _sync_engine.set(engine)


def init_async_db(url: str, **kwargs):
    engine = create_async_engine(url, pool_pre_ping=True, **kwargs)
    _async_engine.set(engine)


@contextmanager
def sync_engine():
    engine = _sync_engine.get()
    if engine is None:
        raise RuntimeError("Synchronous engine is not initialized.")

    with engine.begin() as connection:
        try:
            yield connection
        finally:
            connection.close()


@asynccontextmanager
async def async_engine():
    engine = _async_engine.get()
    if engine is None:
        raise RuntimeError("Asynchronous engine is not initialized.")

    async with engine.begin() as connection:
        try:
            yield connection
        finally:
            await connection.close()
