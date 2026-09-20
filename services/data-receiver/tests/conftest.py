import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI
from src.routes import router
from src.base import Base
from src.models import Device
from src.redis_client import get_redis

@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(router)

    return app

@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    TestSessionLocal = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    try:
        yield TestSessionLocal
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()

@pytest.fixture
def test_device(db_session):
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    device = Device(
        device_id="test-device",
        public_key=public_key.public_bytes_raw(),
    )

    with db_session() as session:
        session.add(device)
        session.commit()

    return device, private_key

@pytest.fixture
def redis_mock(test_app):
    mock = AsyncMock()

    test_app.dependency_overrides[get_redis] = lambda: mock

    yield mock

    test_app.dependency_overrides.clear()


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as client:
        yield client