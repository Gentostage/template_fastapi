from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.logic.metric import create_metric, get_metrics_by_service
from app.schemas.metric import MetricCreate, MetricResponse, MetricServiceResponse

router = APIRouter()


@router.post("/metrics", response_model=MetricResponse)
async def add_metric(metric_data: MetricCreate, session: AsyncSession = Depends(get_async_session)):
    return await create_metric(
        session,
        path=metric_data.path,
        response_time_ms=metric_data.response_time_ms,
        service_name=metric_data.service_name,
    )


@router.get("/metrics/{service_name}", response_model=list[MetricServiceResponse])
async def get_metrics(service_name: str, session: AsyncSession = Depends(get_async_session)):
    return await get_metrics_by_service(session, service_name)
