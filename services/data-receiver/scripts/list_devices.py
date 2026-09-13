from src.database import engine
from src.models import Device
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_devices():
    with Session(engine) as session:
        names = session.scalars(select(Device.device_id)).all()

        for name in names:
            print(name)

if __name__ == "__main__":
    get_devices()