from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.crud.metric import MetricCRUD
from app.models.metric import Metric
from app.schemas.metric import MetricBase


class MetricFactory(ModelFactory[MetricBase]):
    __model__ = MetricBase
    __table__ = Metric

    @classmethod
    async def build_and_save(cls, session: AsyncSession, **kwargs) -> MetricBase:
        payload = cls.build(**kwargs).dict()
        crud = MetricCRUD(session)
        return await crud.create(**payload)
