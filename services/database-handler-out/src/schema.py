from typing import Literal
from datetime import datetime
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

class TelemetryCurrentOut(BaseModel):
    temperature: float
    humidity: float
    pressure: float

class NodeResponseList(BaseModel):
    device: str
    readings: int # readings today
    timestamp: datetime
    rssi: int
    uptime: int
    reset: str

class NodeResponseOut(BaseModel):
    data: list[NodeResponseList]

class TelemetrySummaryList(BaseModel):
    reading: str # avg, high, low
    temp: float
    humidity: float
    pressure: float

class TelemetrySummaryOut(BaseModel):
    data: list[TelemetrySummaryList]