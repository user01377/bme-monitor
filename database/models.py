import datetime
import enum
from sqlalchemy import DateTime, func, Float, Enum, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Status(str, enum.Enum):
    VALID = "valid_reading"
    AUTOFLAGGED = "automatically_flagged"
    MANUAL_INC = "manually_included"
    MANUAL_EXC = "manually_excluded"

class Base(DeclarativeBase):
    pass

class SensorReads(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    device: Mapped[str] = mapped_column(String)

    temp: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    pressure: Mapped[float] = mapped_column(Float)

    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.VALID)

    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
