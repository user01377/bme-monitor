import os
import logging
import logging.config
import json
import datetime
import asyncio

import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import SensorReads, DiagnosticData, Status
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

def process_payload(json_data, session):
    """
    Helper function to process data from REDIS queue.
    Makes unit testing easier for proccessing data.
    """

    # scale down data back to original size
    temperature = json_data["data"]["temperature"] / 100
    humidity = json_data["data"]["humidity"] / 100
    pressure = json_data["data"]["pressure"] / 100

    # convert temp from fahrenheit to celcius
    converted_temp = round((temperature * 9/5) + 32, 2)


    device = json_data["device_id"]
    timestamp = datetime.datetime.fromtimestamp(
            json_data["timestamp"],
            tz=datetime.timezone.utc,
        )

    # create sensor reading object
    sensor_read = SensorReads(
        device=device,
        temp=converted_temp,
        humidity=humidity,
        pressure=pressure,
        status=Status.VALID,
        timestamp=timestamp
    )

    diag_data = DiagnosticData(
        device=device,
        rssi=json_data["diagnostics"]["rssi"],
        uptime=json_data["diagnostics"]["uptime"],
        reset=json_data["diagnostics"]["reset"],
    )

    session.add(sensor_read)
    session.add(diag_data)
    session.commit()

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

            with SessionLocal() as session:
                process_payload(json_data, session)

            logger.info("Data successfully written to PostgreSQL for '%s'", json_data["device_id"])

        except Exception:
            logger.exception("Failed to process telemetry payload")


if __name__ == "__main__":
    asyncio.run(main())