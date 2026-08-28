import datetime
from sqlalchemy import Numeric, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class SensorReads(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True)

    temp: Mapped[float] = mapped_column(Numeric)
    humidity: Mapped[float] = mapped_column(Numeric)
    pressure: Mapped[float] = mapped_column(Numeric)

    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
