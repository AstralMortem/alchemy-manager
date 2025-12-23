# miniorm/session.py
from contextvars import ContextVar
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from contextlib import contextmanager, asynccontextmanager
from .engine import _sync_engine, _async_engine

_sync_session: ContextVar[Session | None] = ContextVar("sync_session", default=None)
_async_session: ContextVar[AsyncSession | None] = ContextVar(
    "async_session", default=None
)

session_factory = None
async_session_factory = None


@contextmanager
def sync_session_scope(auto_commit: bool = False):
    global session_factory
    if session_factory is None:
        engine = _sync_engine.get()
        if engine is None:
            raise RuntimeError("Synchronous engine is not initialized.")
        else:
            session_factory = sessionmaker(bind=engine, expire_on_commit=False)

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
    if async_session_factory is None:
        engine = _async_engine.get()
        if engine is None:
            raise RuntimeError("Synchronous engine is not initialized.")
        else:
            async_session_factory = async_sessionmaker(
                bind=engine, expire_on_commit=False
            )

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
