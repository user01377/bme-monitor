FROM python:3.14-slim AS base

WORKDIR /app

COPY pyproject.toml .

COPY logging.yaml .

COPY src/ ./src/

COPY alembic/ ./alembic/

COPY alembic.ini .

COPY scripts/ ./scripts/

RUN pip install --no-cache-dir .

FROM base AS test

RUN pip install ".[test]"

RUN pip install --no-cache-dir ".[test]"

COPY tests/ ./tests

CMD ["pytest", "-q", "--strict-markers"]

FROM base as production

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003", "--log-config", "logging.yaml"]