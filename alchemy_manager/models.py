from typing import TYPE_CHECKING, ClassVar, Self
from alchemy_manager.session import async_session_scope, sync_session_scope
from sqlalchemy.orm import DeclarativeBase, declared_attr
from .manager import Manager


class ModelMixin:
    # -------- sync --------
    def save(self):
        with sync_session_scope() as session:
            session.add(self)
            session.commit()
        return self

    def delete(self):
        with sync_session_scope() as session:
            session.delete(self)
            session.commit()
        return None

    # -------- async --------
    async def asave(self):
        async with async_session_scope() as session:
            session.add(self)
            await session.commit()
        return self

    async def adelete(self):
        async with async_session_scope() as session:
            await session.delete(self)
            await session.commit()
        return None


class Model(DeclarativeBase, ModelMixin):
    if TYPE_CHECKING:
        objects: ClassVar[Manager[Self]]
    else:

        @declared_attr
        @classmethod
        def objects(cls):
            return Manager(cls)
