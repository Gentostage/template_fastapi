from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class MetricBase(BaseModel):
    service_name: str
    path: str
    response_time_ms: int


class MetricCreate(MetricBase):
    pass


class MetricResponse(MetricBase):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)


class MetricServiceResponse(BaseModel):
    path: str
    average: float
    min: int
    max: int
    p99: float

    model_config = SettingsConfigDict(from_attributes=True)
