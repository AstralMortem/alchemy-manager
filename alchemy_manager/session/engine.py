from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

_sync_engine = ContextVar[Engine | None]("sync_engine", default=None)
_async_engine = ContextVar[AsyncEngine | None]("async_engine", default=None)

_sync_engine_global: Engine | None = None
_async_engine_global: AsyncEngine | None = None


def init_sync_db(url: str, **kwargs):
    global _sync_engine_global
    engine = create_engine(url, pool_pre_ping=True, **kwargs)
    _sync_engine.set(engine)
    _sync_engine_global = engine


def init_async_db(url: str, **kwargs):
    global _async_engine_global
    engine = create_async_engine(url, pool_pre_ping=True, **kwargs)
    _async_engine.set(engine)
    _async_engine_global = engine


def get_sync_engine() -> Engine | None:
    engine = _sync_engine.get()
    if engine is not None:
        return engine
    return _sync_engine_global


def get_async_engine() -> AsyncEngine | None:
    engine = _async_engine.get()
    if engine is not None:
        return engine
    return _async_engine_global


@contextmanager
def sync_engine():
    engine = get_sync_engine()
    if engine is None:
        raise RuntimeError("Synchronous engine is not initialized.")

    with engine.begin() as connection:
        try:
            yield connection
        finally:
            connection.close()


@asynccontextmanager
async def async_engine():
    engine = get_async_engine()
    if engine is None:
        raise RuntimeError("Asynchronous engine is not initialized.")

    async with engine.begin() as connection:
        try:
            yield connection
        finally:
            await connection.close()
