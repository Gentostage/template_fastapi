import uuid

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = mapped_column(String, index=True)
    path = mapped_column(String, index=True)
    response_time_ms = mapped_column(Integer)
