from typing import Literal
import datetime
from pydantic import BaseModel

class AvgDataOut(BaseModel):
    temperature: float
    humidity: float
    pressure: float

class TelemetryPoint(BaseModel):
    timestamp: datetime
    value: float

class TelemetryOut(BaseModel):
    metric: Literal["temp", "humidity", "pressure"]
    data: list[TelemetryPoint]