import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.models import Base
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