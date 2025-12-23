from alchemy_manager.session.engine import _async_engine, _sync_engine
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
