from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.metric import create_metric as crud_create_metric
from app.crud.metric import get_metrics_by_service as crud_get_metrics_by_service
from app.schemas.metric import MetricBase, MetricResponse, MetricServiceResponse


async def create_metric(session: AsyncSession, service_name: str, path: str, response_time_ms: int) -> MetricBase:
    result = await crud_create_metric(session, path=path, response_time_ms=response_time_ms, service_name=service_name)
    return MetricResponse.model_validate(result)


async def get_metrics_by_service(session: AsyncSession, service_name: str) -> list[MetricBase]:
    result = await crud_get_metrics_by_service(session, service_name)
    return [MetricServiceResponse.model_validate(metric) for metric in result]
