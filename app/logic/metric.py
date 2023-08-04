from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.metric import MetricCRUD
from app.schemas.metric import MetricBase, MetricServiceResponse


async def create_metric(session: AsyncSession, service_name: str, path: str, response_time_ms: int) -> MetricBase:
    metric_crud = MetricCRUD(session)
    return await metric_crud.create(path=path, response_time_ms=response_time_ms, service_name=service_name)


async def get_metrics_by_service(session: AsyncSession, service_name: str) -> list[MetricBase]:
    metric_crud = MetricCRUD(session)
    result = await metric_crud.get_metrics_by_service(service_name)
    return [MetricServiceResponse.model_validate(metric) for metric in result]
