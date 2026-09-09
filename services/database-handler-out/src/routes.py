from fastapi import APIRouter, Depends

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import get_db
from .models import SensorReads, Status
from .schema import AvgDataOut

router = APIRouter()

@router.get("/health")
def get_health():
    return {"status": "ok"}

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