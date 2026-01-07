from alchemy_manager.queryset import QuerySet
from alchemy_manager.queryset.queryset import ModelT
from alchemy_manager.session import async_session_scope, sync_session_scope
from typing import Generic, Type


class Manager(Generic[ModelT]):
    def __init__(self, model: Type[ModelT]):
        self.model = model

    def filter(self, *q, **kw) -> QuerySet[ModelT]:
        return QuerySet(self.model).filter(*q, **kw)

    # -------- sync --------
    def get(self, **kw) -> ModelT:
        obj = self.filter(**kw).first()
        if not obj:
            raise LookupError("Object does not exist")
        return obj
    
    def get_or_none(self, **kw) -> ModelT | None:
        return self.filter(**kw).first()
    
    def all(self) -> list[ModelT]:
        return self.filter().all()

    def create(self, **kw) -> ModelT:
        with sync_session_scope() as session:
            obj = self.model(**kw)
            session.add(obj)
            session.commit()
        return obj

    def bulk_create(self, objs: list) -> list[ModelT]:
        with sync_session_scope() as session:
            session.add_all(objs)
            session.commit()
        return objs

    # -------- async --------
    async def aget(self, **kw) -> ModelT:
        obj = await self.filter(**kw).afirst()
        if not obj:
            raise LookupError("Object does not exist")
        return obj
    
    async def aget_or_none(self, **kw) -> ModelT | None:
        return await self.filter(**kw).afirst()
    
    async def aall(self) -> list[ModelT]:
        return await self.filter().aall()

    async def acreate(self, **kw) -> ModelT:
        async with async_session_scope() as session:
            obj = self.model(**kw)
            session.add(obj)
            await session.commit()
        return obj

    async def abulk_create(self, objs: list) -> list[ModelT]:
        async with async_session_scope() as session:
            session.add_all(objs)
            await session.commit()
        return objs
