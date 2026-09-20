import pytest
import hashlib
import secrets
import datetime
from sqlalchemy import StaticPool, create_engine

from src.models import ApiToken
from src.models import Base
from src.main import app
from src.database import get_db
from sqlalchemy.orm import sessionmaker

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

@pytest.fixture
def test_token():
    return secrets.token_urlsafe(32)

@pytest.fixture
def test_api_token(db_session, test_token):
    token_hash = hashlib.sha256(test_token.encode()).hexdigest()

    api_token = ApiToken(
        token_hash=token_hash,
        name="test-token",
    )

    db_session.add(api_token)
    db_session.commit()
    db_session.refresh(api_token)

    return api_token

@pytest.fixture
def revoked_api_token(db_session):
    token = secrets.token_urlsafe(32)

    api_token = ApiToken(
        token_hash=hashlib.sha256(token.encode()).hexdigest(),
        name="revoked-test-token",
        revoked_at=datetime.datetime.now(datetime.UTC),
    )

    db_session.add(api_token)
    db_session.commit()
    db_session.refresh(api_token)

    return token