from typing import Literal
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class Status(str, Enum):
    VALID = "valid_reading"
    AUTOFLAGGED = "automatically_flagged"
    MANUAL_INC = "manually_included"
    MANUAL_EXC = "manually_excluded"

class TrendEnum(str, Enum):
    UP = "up"
    DOWN = "down"
    NEUTRAL = "neutral"

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
    timestamp: datetime

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
    reading: str # 3 types of readings returned: avg, high, low
    temp: float
    humidity: float
    pressure: float

class TelemetrySummaryOut(BaseModel):
    data: list[TelemetrySummaryList]

class TelemetryTrendsList(BaseModel):
    device: str
    temp: TrendEnum
    humidity: TrendEnum
    pressure: TrendEnum

class TelemetryTrendsOut(BaseModel):
    data: list[TelemetryTrendsList]