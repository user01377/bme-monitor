import os
import logging
import logging.config
import json
import datetime
import asyncio

import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import SensorReads, Status
from .redis_client import connect_redis

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database_url = f"postgresql+psycopg://{user}:{password}@db:5432/bme280"

engine = create_engine(database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

with open("logging.yaml") as f:
    logging.config.dictConfig(yaml.safe_load(f))

logger = logging.getLogger(__name__)


async def main():
    redis = await connect_redis()

    logger.info("Service started, querying REDIS for jobs..")

    while True:
        _, data = await redis.brpop("data_queue")

        logger.info("Grabbed a payload from the queue")

        try:
            json_data = json.loads(data)
            # debugging log
            # logger.info("JSON DATA: %s", json_data)

            # scale down data back to original size
            json_data["data"]["temperature"] /= 100
            json_data["data"]["humidity"] /= 100
            json_data["data"]["pressure"] /= 100

            converted_temp = (json_data["data"]["temperature"] * 9/5) + 32

            with SessionLocal() as session:
                sensor_read = SensorReads(
                    device=json_data["device_id"],
                    temp=converted_temp,
                    humidity=json_data["data"]["humidity"],
                    pressure=json_data["data"]["pressure"],
                    status=Status.VALID,
                    timestamp=datetime.datetime.fromtimestamp(
                        json_data["timestamp"],
                        tz=datetime.timezone.utc,
                    ),
                )

                session.add(sensor_read)
                session.commit()

            logger.info("Data successfully written to PostgreSQL for '%s'", json_data["device_id"])

        except Exception:
            logger.exception("Failed to process telemetry payload")


asyncio.run(main())