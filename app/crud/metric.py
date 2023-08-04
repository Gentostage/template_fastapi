from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metric import Metric


async def create_metric(session: AsyncSession, service_name: str, path: str, response_time_ms: int) -> Metric:
    metric = Metric(service_name=service_name, path=path, response_time_ms=response_time_ms)
    session.add(metric)
    await session.commit()
    await session.refresh(metric)
    return metric


async def get_metrics_by_service(session: AsyncSession, service_name: str) -> list[dict]:
    query = (
        select(
            Metric.path,
            func.avg(Metric.response_time_ms).label("average"),
            func.min(Metric.response_time_ms).label("min"),
            func.max(Metric.response_time_ms).label("max"),
            func.percentile_cont(0.99).within_group(Metric.response_time_ms).label("p99"),
        )
        .where(Metric.service_name == service_name)
        .group_by(Metric.path)
    )

    raws = (await session.execute(query)).all()

    result = []
    for path, average, min_time, max_time, p99 in raws:
        metrics_data = {
            "path": path,
            "average": average,
            "min": min_time,
            "max": max_time,
            "p99": p99,
        }
        result.append(metrics_data)
    return result
