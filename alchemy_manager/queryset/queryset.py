# miniorm/queryset.py
from sqlalchemy import select, update, delete
from alchemy_manager.session import sync_session_scope, async_session_scope
from .q import Q
from typing import Self, Type, TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from alchemy_manager.models import Model

ModelT = TypeVar("ModelT", bound="Model")


class QuerySet(Generic[ModelT]):
    def __init__(self, model: Type[ModelT], stmt=None):
        self.model = model
        self.stmt = stmt if stmt is not None else select(model)

    def filter(self, *q_objects: Q, **kwargs) -> "QuerySet[ModelT]":
        stmt = self.stmt

        for q in q_objects:
            stmt = stmt.where(q.resolve(self.model))

        if kwargs:
            stmt = stmt.where(Q(**kwargs).resolve(self.model))

        return QuerySet(self.model, stmt)

    # ---------- sync ----------
    def all(self) -> list[ModelT]:
        with sync_session_scope() as session:
            return session.execute(self.stmt).scalars().all()

    def first(self) -> ModelT | None:
        with sync_session_scope() as session:
            return session.execute(self.stmt.limit(1)).scalars().first()

    def update(self, **values) -> None:
        with sync_session_scope() as session:
            stmt = update(self.model).where(*self.stmt._where_criteria).values(**values)
            result = session.execute(stmt)
            session.commit()

    def delete(self) -> None:
        with sync_session_scope() as session:
            stmt = delete(self.model).where(*self.stmt._where_criteria)
            session.execute(stmt)
            session.commit()

    # ---------- async ----------
    async def aall(self) -> list[ModelT]:
        async with async_session_scope() as session:
            result = await session.execute(self.stmt)
            return result.scalars().all()

    async def afirst(self) -> ModelT | None:
        async with async_session_scope() as session:
            result = await session.execute(self.stmt.limit(1))
            return result.scalars().first()

    async def aupdate(self, **values) -> None:
        async with async_session_scope() as session:
            stmt = update(self.model).where(*self.stmt._where_criteria).values(**values)
            await session.execute(stmt)
            await session.commit()

    async def adelete(self) -> None:
        async with async_session_scope() as session:
            stmt = delete(self.model).where(*self.stmt._where_criteria)
            await session.execute(stmt)
            await session.commit()
