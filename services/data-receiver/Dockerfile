FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .

COPY logging.yaml .

COPY src/ ./src/

COPY alembic/ ./alembic/

COPY alembic.ini .

COPY scripts/ ./scripts/

RUN pip install --no-cache-dir .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging.yaml"]