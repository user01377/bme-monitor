FROM python:3.14-slim AS base

COPY --from=astral/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY logging.yaml .

COPY src/ ./src/

FROM base AS test

RUN uv sync --frozen --extra test

COPY tests/ ./tests

CMD ["uv", "run", "pytest", "-q", "--strict-markers"]

FROM base AS production

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002", "--log-config", "logging.yaml"]