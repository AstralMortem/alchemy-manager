import asyncio
from alchemy_manager.session.engine import (
    _async_engine,
    _sync_engine,
    get_async_engine,
    get_sync_engine,
)
from alchemy_manager.session import sync_session_scope, async_session_scope

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import pytest


def test_engines_initialized():
    assert _sync_engine.get() is not None
    assert _async_engine.get() is not None


def test_sync_session_scope():
    with sync_session_scope() as session:
        assert isinstance(session, Session)
        assert session.is_active is True


@pytest.mark.asyncio
async def test_async_session_scope():
    async with async_session_scope() as session:
        assert isinstance(session, AsyncSession)
        assert session.is_active is True


@pytest.mark.asyncio
async def test_engines_available_in_new_asyncio_task():
    async def check_engines():
        _sync_engine.set(None)
        _async_engine.set(None)
        return get_sync_engine(), get_async_engine()

    sync_engine_value, async_engine_value = await asyncio.create_task(check_engines())

    assert sync_engine_value is not None
    assert async_engine_value is not None

    async def check_async_session():
        _async_engine.set(None)
        async with async_session_scope() as session:
            return isinstance(session, AsyncSession), session.is_active

    is_async_session, is_active = await asyncio.create_task(check_async_session())
    assert is_async_session is True
    assert is_active is True
