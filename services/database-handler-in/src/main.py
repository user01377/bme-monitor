import logging
import logging.config
import yaml

from .redis_client import connect_redis

with open("logging.yaml") as f:
    logging.config.dictConfig(yaml.safe_load(f))

logger = logging.getLogger(__name__)

redis = connect_redis

while True:
    logger.info("Service started, querying REDIS for jobs..")

    