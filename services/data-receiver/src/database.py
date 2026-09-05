from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .models import Device

DATABASE_URL = "sqlite:///./devices.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_device(device_id: str):
    with SessionLocal() as session:
        result = session.execute(select(Device).where(Device.device_id == device_id))

        return result.scalar_one_or_none()