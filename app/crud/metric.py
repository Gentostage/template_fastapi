from sqlalchemy import func, select

from app.crud.base import BaseCRUD
from app.models.metric import Metric


class MetricCRUD(BaseCRUD):
    model: Metric = Metric

    async def get_metrics_by_service(self, service_name: str) -> list[dict]:
        query = (
            select(
                self.model.path,
                func.avg(self.model.response_time_ms).label("average"),
                func.min(self.model.response_time_ms).label("min"),
                func.max(self.model.response_time_ms).label("max"),
                func.percentile_cont(0.99).within_group(self.model.response_time_ms).label("p99"),
            )
            .where(self.model.service_name == service_name)
            .group_by(self.model.path)
        )

        raws = (await self.session.execute(query)).all()

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
