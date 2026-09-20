FROM python:3.14-slim AS base

WORKDIR /app

COPY pyproject.toml .

COPY logging.yaml .

COPY src/ ./src/

RUN pip install --no-cache-dir .

FROM base AS test

RUN pip install ".[test]"

RUN pip install --no-cache-dir ".[test]"

COPY tests/ ./tests

CMD ["pytest", "-q", "--strict-markers"]

FROM base AS production

CMD ["python", "-m" ,"src.main"]