import logging
from typing import Literal
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import get_db
from .models import SensorReads, DiagnosticData, Status
from .schema import TelemetryOut, TelemetryPoint, TelemetryCurrentOut, NodeResponseOut, NodeResponseList, TelemetrySummaryOut, TelemetrySummaryList, TelemetryTrendsOut, TelemetryTrendsList, TrendEnum

# variable for how far back the trend data should be compared against /telemetry/trend
COMPARE_PAST_HOURS = 3

logger = logging.getLogger(__name__)

router = APIRouter()

def verify_device(device_id: str, db) -> bool:
    stmt = (
        select(SensorReads.device)
        .where(SensorReads.device == device_id)
        .limit(1)
    )

    return db.execute(stmt).scalar_one_or_none() is not None

def calculate_start_end_day() -> tuple[datetime, datetime]:
    # defines what the start and end time of the current day is
    
    current_zone = ZoneInfo("America/New_York")
    start_local = datetime.now(current_zone).replace(hour=0, minute=0, second=0, microsecond=0)

    start_time = start_local.astimezone(timezone.utc)
    end_time = (start_local + timedelta(days=1)).astimezone(timezone.utc)

    return start_time, end_time

def calculate_trend(current: float, average: float) -> TrendEnum:
    """
    Helper function for calculating the enum value for the current trend in telemetry data
    """
    if current > average:
        return TrendEnum.UP
    elif current < average:
        return TrendEnum.DOWN
    
    return TrendEnum.NEUTRAL

@router.get("/telemetry", response_model=TelemetryOut)
def get_telemetry(device_id: str, metric: Literal["temp", "humidity", "pressure"], range: int = 24, db: Session = Depends(get_db)):

    if not verify_device(device_id, db):
        raise HTTPException(status_code=404, detail="Device Not Found")

    # maps string to database column
    metric_column = {
        "temp": SensorReads.temp,
        "humidity": SensorReads.humidity,
        "pressure": SensorReads.pressure,
    }

    start_time = datetime.now(timezone.utc) - timedelta(hours=range)

    stmt = (
        select(SensorReads.timestamp, metric_column[metric])
        .where(
            SensorReads.device == device_id,
            SensorReads.timestamp >= start_time
        )
        .order_by(SensorReads.timestamp)
    )

    data = db.execute(stmt).all()

    if (len(data) == 0):
        raise HTTPException(status_code=404, detail="No Readings In Time Period")

    return TelemetryOut(
        metric=metric,
        data=[TelemetryPoint(timestamp=row[0], value=row[1]) for row in data]
    )

@router.get("/telemetry/current", response_model=TelemetryCurrentOut)
def get_current_data(device_id: str, db: Session = Depends(get_db)):

    if not verify_device(device_id, db):
        raise HTTPException(status_code=404, detail="Device Not Found")
    
    stmt = (
        select(SensorReads.temp, SensorReads.humidity, SensorReads.pressure)
        .where(SensorReads.device == device_id)
        .order_by(SensorReads.timestamp.desc())
        .limit(1)
    )

    data = db.execute(stmt).one_or_none()

    if data is None:
        raise HTTPException(status_code=404, detail="No Readings Found")

    return TelemetryCurrentOut(
        temperature=data[0],
        humidity=data[1],
        pressure=data[2]
    )

@router.get("/nodes", response_model=NodeResponseOut)
def get_diag_nodes(device_id: str | None = None, db: Session = Depends(get_db)):

    if device_id and not verify_device(device_id, db):
        raise HTTPException(status_code=404, detail="Device Not Found")
    
    start_time, end_time = calculate_start_end_day()
    
    stmt = (
        select(DiagnosticData.device, DiagnosticData.timestamp, DiagnosticData.rssi, DiagnosticData.uptime, DiagnosticData.reset)
        .distinct(DiagnosticData.device)
        .order_by(
            DiagnosticData.device,
            DiagnosticData.timestamp.desc()
        )
    )

    count_stmt = (
        select(SensorReads.device, func.count(SensorReads.id).label("readings"))
        .where(
            SensorReads.timestamp >= start_time,
            SensorReads.timestamp < end_time,
        )
        .group_by(SensorReads.device)
    )

    if device_id:
        stmt = stmt.where(DiagnosticData.device == device_id)
        count_stmt = count_stmt.where(SensorReads.device == device_id)

    data = db.execute(stmt).all()

    # creates a dictionary which maps device_id to its readings for that day
    current_reading_count = {row.device: row.readings for row in db.execute(count_stmt).all()}

    return NodeResponseOut(
        data=[NodeResponseList(
            device=row[0],
            readings=current_reading_count.get(row[0], 0), # use dictionary created to get reading count associated with the device_id, default to zero if no readings exist.
            timestamp=row[1],
            rssi=row[2],
            uptime=row[3],
            reset=row[4]
        ) for row in data]
    )

@router.get("/telemetry/summary", response_model=TelemetrySummaryOut)
def get_telemetry_summary(db: Session = Depends(get_db)):

    start_time, end_time = calculate_start_end_day()

    avg_stmt = (
        select(func.avg(SensorReads.temp), func.avg(SensorReads.humidity), func.avg(SensorReads.pressure))
        .where(
            SensorReads.timestamp >= start_time,
            SensorReads.timestamp < end_time,
        )
    )

    max_stmt = (
        select(func.max(SensorReads.temp), func.max(SensorReads.humidity), func.max(SensorReads.pressure))
        .where(
            SensorReads.timestamp >= start_time,
            SensorReads.timestamp < end_time,
        )
    )

    min_stmt = (
        select(func.min(SensorReads.temp), func.min(SensorReads.humidity), func.min(SensorReads.pressure))
        .where(
            SensorReads.timestamp >= start_time,
            SensorReads.timestamp < end_time,
        )
    )

    avg_data = db.execute(avg_stmt).one();
    max_data = db.execute(max_stmt).one();
    min_data = db.execute(min_stmt).one();

    if avg_data[0] is None:
        raise HTTPException(status_code=404, detail="No Readings Today")

    return TelemetrySummaryOut(
        data=[
            TelemetrySummaryList(
                reading="avg",
                temp=avg_data[0],
                humidity=avg_data[1],
                pressure=avg_data[2]
            ),
            TelemetrySummaryList(
                reading="high",
                temp=max_data[0],
                humidity=max_data[1],
                pressure=max_data[2]
            ),
            TelemetrySummaryList(
                reading="low",
                temp=min_data[0],
                humidity=min_data[1],
                pressure=min_data[2]
            )
        ]
    )

@router.get("/telemetry/trend", response_model=TelemetryTrendsOut)
def get_telemetry_trends(device_id: str | None = None, db: Session = Depends(get_db)):
    
    if device_id and not verify_device(device_id, db):
        raise HTTPException(status_code=404, detail="Device Not Found")
    
    # ex. start time: base trends on data from 3 hours ago
    start_time = datetime.now(timezone.utc) - timedelta(hours=COMPARE_PAST_HOURS)
    
    avg_stmt = (
        select(
            SensorReads.device,
            func.avg(SensorReads.temp).label("temp"),
            func.avg(SensorReads.humidity).label("humidity"),
            func.avg(SensorReads.pressure).label("pressure")
        )
        .where(SensorReads.timestamp >= start_time)
        .group_by(SensorReads.device)
    )

    current_stmt = (
        select(SensorReads.device, SensorReads.temp, SensorReads.humidity, SensorReads.pressure)
        .distinct(SensorReads.device)
        .order_by(
            SensorReads.device,
            SensorReads.timestamp.desc(),
            SensorReads.id.desc()
        )
    )

    if device_id:
        avg_stmt = avg_stmt.where(SensorReads.device == device_id)
        current_stmt = current_stmt.where(SensorReads.device == device_id)

    average_data = db.execute(avg_stmt).all()
    current_data = db.execute(current_stmt).all()

    current_dict = {
        row.device: row
        for row in current_data
    }

    return TelemetryTrendsOut(
        data=[TelemetryTrendsList(
            device=average_row.device,
            temp=calculate_trend(current_dict.get(average_row.device).temp, average_row.temp),
            humidity=calculate_trend(current_dict.get(average_row.device).humidity, average_row.humidity),
            pressure=calculate_trend(current_dict.get(average_row.device).pressure, average_row.pressure)
        ) for average_row in average_data]
    )