from .models import User
import pytest


def test_create_and_get():
    user = User.objects.create(name="Alice", age=20)
    assert user.id is not None

    fetched = User.objects.get(id=user.id)
    assert fetched.name == "Alice"


def test_bulk_create():
    users = User.objects.bulk_create(
        [
            User(name="A"),
            User(name="B"),
        ]
    )
    assert len(users) == 2


@pytest.mark.asyncio
async def test_async_create_and_get():
    user = await User.objects.acreate(name="Bob", age=30)
    assert user.id is not None

    fetched = await User.objects.aget(id=user.id)
    assert fetched.name == "Bob"
