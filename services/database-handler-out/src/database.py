import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database_url = f"postgresql+psycopg://{user}:{password}@db:5432/bme280"

engine = create_engine(database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False
)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()