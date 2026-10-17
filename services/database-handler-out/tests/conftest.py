import pytest
import datetime
from datetime import timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.models import Base, SensorReads, Status
from src.database import get_db
from src.main import app

@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    def override_get_db():
        yield session
    
    app.dependency_overrides[get_db] = override_get_db

    try:
        yield session
    finally:
        app.dependency_overrides.clear()
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()

@pytest.fixture()
def seeded_db(db_session):
    db_session.add_all([
        SensorReads(
            device="test-device",
            temp=20,
            humidity=40,
            pressure=1000,
            status=Status.VALID,
            timestamp=datetime.datetime.now(datetime.UTC)
            - datetime.timedelta(hours=2),
        ),
        SensorReads(
            device="test-device",
            temp=20,
            humidity=40,
            pressure=1000,
            status=Status.VALID,
            timestamp=datetime.datetime.now(datetime.UTC)
            - datetime.timedelta(hours=3),
        ),
        SensorReads(
            device="test-device",
            temp=30,
            humidity=60,
            pressure=1020,
            status=Status.VALID,
            timestamp=datetime.datetime.now(datetime.UTC)
            - datetime.timedelta(hours=6),
        ),
    ])

    db_session.commit()

    return db_session

@pytest.fixture()
def seeded_summary_db(db_session):
    # Get midnight of the current day in New York
    today = datetime.datetime.now(ZoneInfo("America/New_York"))

    start = today.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    readings = [
        (20, 40, 1000),
        (20, 40, 1000),
        (30, 60, 1020),
    ]

    for i, (temp, humidity, pressure) in enumerate(readings):
        db_session.add(
            SensorReads(
                device="test-device",
                temp=temp,
                humidity=humidity,
                pressure=pressure,
                status=Status.VALID,
                timestamp=(
                    start + timedelta(minutes=i)
                ).astimezone(timezone.utc)
            )
        )

    db_session.commit()

    return db_session