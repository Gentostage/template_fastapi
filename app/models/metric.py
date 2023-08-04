from sqlalchemy import Integer, String
from app.models.base import Base
from sqlalchemy.orm import mapped_column


class Metric(Base):
    __tablename__ = "metrics"

    id = mapped_column(Integer, primary_key=True, index=True)
    service_name = mapped_column(String, index=True)
    path = mapped_column(String, index=True)
    response_time_ms = mapped_column(Integer)