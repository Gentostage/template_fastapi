import select
from typing import Any, Type, TypeVar

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD:
    model: Type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Type[ModelType]:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, pk: str, value: Any) -> Type[ModelType]:
        """Может поднять sqlalchemy.exc.NoResultFound"""
        query = select(self.model).where(getattr(self.model, pk) == value)
        instance = (await self.session.execute(query)).unique().scalars().one()
        return instance

    async def read(self, pk: str, value: Any) -> Type[ModelType]:
        """Может поднять sqlalchemy.exc.NoResultFound"""
        query = select(self.model).where(getattr(self.model, pk) == value)
        instance = (await self.session.execute(query)).unique().scalars().all()
        return instance

    async def update(self, pk: str, **kwargs) -> Type[ModelType]:
        query = update(self.model).where(getattr(self.model, pk) == kwargs[pk]).values(**kwargs)
        result = await self.session.execute(query)
        await self.session.commit()
        return result

    async def delete(
        self,
        pk: str,
        value: Any,
    ) -> None:
        query = delete(self.mode).where(getattr(self.model, pk) == value)
        await self.session.execute(query)
        await self.session.commit()
