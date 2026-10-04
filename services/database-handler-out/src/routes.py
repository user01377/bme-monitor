from fastapi import APIRouter, Depends

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import get_db
from .models import SensorReads, Status
from .schema import AvgDataOut

router = APIRouter()

@router.get("/telemetry")
async def get_current_data(metric: str, range: int, db: Session = Depends(get_db)):
    return

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