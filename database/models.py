import datetime
from sqlalchemy import DateTime, func, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class SensorReads(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True)

    temp: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    pressure: Mapped[float] = mapped_column(Float)

    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
