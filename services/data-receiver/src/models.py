from sqlalchemy import LargeBinary, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Device(Base):
    __tablename__ = "devices"

    device_id: Mapped[str] = mapped_column(Text, primary_key=True, unique=True)
    public_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)