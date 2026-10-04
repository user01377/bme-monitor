from typing import Literal
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import get_db
from .models import SensorReads, Status
from .schema import AvgDataOut, TelemetryOut, TelemetryPoint

router = APIRouter()

@router.get("/telemetry", response_model=TelemetryOut)
async def get_current_data(metric: Literal["temp", "humidity", "pressure"], range: int = 24, device_id: str | None = None, db: Session = Depends(get_db)):
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
            SensorReads.timestamp >= start_time
        )
        .order_by(SensorReads.timestamp)
    )

    if device_id:
        stmt = stmt.where(SensorReads.device_id == device_id)

    data = db.execute(stmt).all()

    return TelemetryOut(
        metric=metric,
        data=[TelemetryPoint(timestamp=row[0], value=row[1]) for row in data]
    )

@router.get("/telemetry/current")
async def get_current_data(device_id: str, db: Session = Depends(get_db)):
    return

@router.get("/nodes")
async def get_diag_nodes(db: Session = Depends(get_db)):
    return

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