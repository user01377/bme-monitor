import logging
from typing import Literal
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import get_db
from .models import SensorReads, DiagnosticData, Status
from .schema import AvgDataOut, TelemetryOut, TelemetryPoint, TelemetryCurrentOut, NodeResponseOut, NodeResponseList

logger = logging.getLogger(__name__)

router = APIRouter()

def verify_device(device_id: str, db) -> bool:
    stmt = (
        select(SensorReads.device)
        .where(SensorReads.device == device_id)
        .limit(1)
    )

    return db.execute(stmt).scalar_one_or_none() is not None

@router.get("/telemetry", response_model=TelemetryOut)
async def get_telemetry(device_id: str, metric: Literal["temp", "humidity", "pressure"], range: int = 24, db: Session = Depends(get_db)):

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
async def get_current_data(device_id: str, db: Session = Depends(get_db)):

    if not verify_device(device_id, db):
        raise HTTPException(status_code=404, detail="Device Not Found")
    
    stmt = (
        select(SensorReads.temp, SensorReads.humidity, SensorReads.pressure)
        .where(SensorReads.device == device_id)
        .order_by(SensorReads.timestamp.desc())
        .limit(1)
    )

    data = db.execute(stmt).one_or_none()

    return TelemetryCurrentOut(
        temperature=data[0],
        humidity=data[1],
        pressure=data[2]
    )

@router.get("/nodes", response_model=NodeResponseOut)
async def get_diag_nodes(device_id: str | None = None, db: Session = Depends(get_db)):
    
    stmt = (
        select(DiagnosticData.device, DiagnosticData.timestamp, DiagnosticData.rssi, DiagnosticData.uptime, DiagnosticData.reset)
        .distinct(DiagnosticData.device)
        .order_by(
            DiagnosticData.device,
            DiagnosticData.timestamp.desc()
        )
    )

    if device_id:
        stmt = stmt.where(DiagnosticData.device == device_id)

    data = db.execute(stmt).all()

    return NodeResponseOut(
        data=[NodeResponseList(
            device=row[0],
            timestamp=row[1],
            rssi=row[2],
            uptime=row[3],
            reset=row[4]
        ) for row in data]
    )

@router.get("/average", response_model=AvgDataOut)
def get_data(db: Session = Depends(get_db)):
    """
    Returns AVG of each data point
    """

    stmt = select(
    func.avg(SensorReads.temp).label("temperature"),
    func.avg(SensorReads.humidity).label("humidity"),
    func.avg(SensorReads.pressure).label("pressure"),
    ).where(
        SensorReads.status.in_([
            Status.VALID,
            Status.MANUAL_INC
        ])
    )

    result = db.execute(stmt).one()

    return AvgDataOut(
        temperature=result.temperature,
        humidity=result.humidity,
        pressure=result.pressure
    )