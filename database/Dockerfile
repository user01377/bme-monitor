FROM python:3.14-slim

COPY --from=astral/uv:latest /uv /uvx /bin/

WORKDIR /database
ENV PATH="/database/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

CMD ["alembic", "upgrade", "head"]