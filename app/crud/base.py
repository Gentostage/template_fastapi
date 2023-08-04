from typing import Type, TypeVar

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
