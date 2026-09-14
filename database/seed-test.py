import datetime

import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import SensorReads, Status


load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql+psycopg://{user}:{password}@localhost:5432/bme280"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def seed():
    db = SessionLocal()

    try:
        readings = [
            SensorReads(
                device="esp32-01",
                temp=22.4,
                humidity=48.2,
                pressure=1012.4,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(minutes=30),
            ),
            SensorReads(
                device="esp32-01",
                temp=22.7,
                humidity=47.9,
                pressure=1012.7,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(minutes=20),
            ),
            SensorReads(
                device="esp32-01",
                temp=23.1,
                humidity=47.5,
                pressure=1013.0,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(minutes=10),
            ),
            SensorReads(
                device="esp32-01",
                temp=23.4,
                humidity=47.1,
                pressure=1013.2,
                status=Status.VALID,
            ),
            SensorReads(
                device="esp32-01",
                temp=95.0,
                humidity=47.0,
                pressure=1013.1,
                status=Status.AUTOFLAGGED,
            ),
            SensorReads(
                device="esp32-01",
                temp=23.0,
                humidity=46.8,
                pressure=1013.3,
                status=Status.MANUAL_INC,
            ),
            SensorReads(
                device="esp32-02",
                temp=21.8,
                humidity=52.1,
                pressure=1011.9,
                status=Status.VALID,
            ),
            SensorReads(
                device="esp32-02",
                temp=22.1,
                humidity=51.7,
                pressure=1012.2,
                status=Status.VALID,
            ),
        ]

        db.add_all(readings)
        db.commit()

        print(f"Inserted {len(readings)} readings.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()