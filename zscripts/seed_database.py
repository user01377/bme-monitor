"""
!!LOCAL SEED SCRIPT FOR DEV TESTING!!

run this from project root:
python -m zscripts.seed-test
"""

import datetime

import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import SensorReads, DiagnosticData, Status


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

            # SHOULD APPEAR: 30 minutes ago, esp32-01, VALID
            SensorReads(
                device="esp32-01",
                temp=22.4,
                humidity=48.2,
                pressure=1012.4,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(minutes=30),
            ),

            # SHOULD APPEAR: 20 minutes ago, esp32-01, VALID
            SensorReads(
                device="esp32-01",
                temp=22.7,
                humidity=47.9,
                pressure=1012.7,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(minutes=20),
            ),

            # SHOULD APPEAR: 10 minutes ago, esp32-01, VALID
            SensorReads(
                device="esp32-01",
                temp=23.1,
                humidity=47.5,
                pressure=1013.0,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(minutes=10),
            ),

            # SHOULD APPEAR: now, esp32-01, VALID
            SensorReads(
                device="esp32-01",
                temp=23.4,
                humidity=47.1,
                pressure=1013.2,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC),
            ),

            # SHOULD APPEAR: 2 hours ago, esp32-01, AUTOFLAGGED
            # Useful for testing whether status filtering is implemented.
            SensorReads(
                device="esp32-01",
                temp=95.0,
                humidity=47.0,
                pressure=1013.1,
                status=Status.AUTOFLAGGED,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(hours=2),
            ),

            # SHOULD APPEAR: 6 hours ago, esp32-01, MANUAL_INC
            SensorReads(
                device="esp32-01",
                temp=23.0,
                humidity=46.8,
                pressure=1013.3,
                status=Status.MANUAL_INC,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(hours=6),
            ),

            # SHOULD APPEAR: 23 hours ago, esp32-01, VALID
            # Useful for testing the boundary of a 24-hour range.
            SensorReads(
                device="esp32-01",
                temp=21.5,
                humidity=50.2,
                pressure=1011.7,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(hours=23),
            ),

            # SHOULD NOT APPEAR for a 24-hour range: 25 hours ago
            SensorReads(
                device="esp32-01",
                temp=20.9,
                humidity=51.0,
                pressure=1011.2,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(hours=25),
            ),

            # SHOULD NOT APPEAR for a 24-hour range: 7 days ago
            SensorReads(
                device="esp32-01",
                temp=19.8,
                humidity=55.4,
                pressure=1009.8,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(days=7),
            ),

            # SHOULD APPEAR for a 24-hour range: 12 hours ago, esp32-02
            # Useful for testing device_id filtering.
            SensorReads(
                device="esp32-02",
                temp=21.8,
                humidity=52.1,
                pressure=1011.9,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(hours=12),
            ),

            # SHOULD NOT APPEAR for a 24-hour range: 2 days ago, esp32-02
            SensorReads(
                device="esp32-02",
                temp=22.1,
                humidity=51.7,
                pressure=1012.2,
                status=Status.VALID,
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(days=2),
            ),
        ]

        diag_data = [
            DiagnosticData(
                device="esp32-01",
                rssi=-48,
                uptime=86400,
                reset="power_on",
            ),
            DiagnosticData(
                device="esp32-01",
                rssi=-62,
                uptime=604800,
                reset="software",
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(days=2),
            ),
            DiagnosticData(
                device="esp32-01",
                rssi=-71,
                uptime=172800,
                reset="brownout",
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(days=2),
            ),
            DiagnosticData(
                device="esp32-02",
                rssi=-51,
                uptime=90000,
                reset="power_on",
            ),
            DiagnosticData(
                device="esp32-02",
                rssi=-65,
                uptime=612000,
                reset="software",
                timestamp=datetime.datetime.now(datetime.UTC)
                - datetime.timedelta(days=2),
            ),
        ]

        db.add_all(diag_data)
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