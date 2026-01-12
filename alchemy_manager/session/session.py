# miniorm/session.py
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager, asynccontextmanager
from .engine import get_async_engine, get_sync_engine

_sync_session: ContextVar[Session | None] = ContextVar("sync_session", default=None)
_async_session: ContextVar[AsyncSession | None] = ContextVar(
    "async_session", default=None
)

session_factory = None
async_session_factory = None
_sync_session_factory_engine = None
_async_session_factory_engine = None


@contextmanager
def sync_session_scope(auto_commit: bool = False):
    global session_factory
    global _sync_session_factory_engine
    engine = get_sync_engine()
    if engine is None:
        raise RuntimeError("Asynchronous engine is not initialized.")
    if session_factory is None or _sync_session_factory_engine is not engine:
        session_factory = sessionmaker(bind=engine, expire_on_commit=False)
        _sync_session_factory_engine = engine

    with session_factory() as session:
        try:
            _sync_session.set(session)
            yield session
            if auto_commit:
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


@asynccontextmanager
async def async_session_scope(auto_commit: bool = False):
    global async_session_factory
    global _async_session_factory_engine
    engine = get_async_engine()
    if engine is None:
        raise RuntimeError("Synchronous engine is not initialized.")
    if async_session_factory is None or _async_session_factory_engine is not engine:
        async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
        _async_session_factory_engine = engine

    async with async_session_factory() as session:
        try:
            _async_session.set(session)
            yield session
            if auto_commit:
                await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
