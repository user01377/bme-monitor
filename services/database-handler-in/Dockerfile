FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .

COPY logging.yaml .

COPY src/ ./src/

RUN pip install --no-cache-dir .

CMD ["python", "-m" ,"src.main"]