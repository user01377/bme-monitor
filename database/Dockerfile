FROM python:3.14-slim

WORKDIR /database

COPY . .

RUN pip install alembic psycopg[binary] python-dotenv sqlalchemy

CMD ["alembic", "upgrade", "head"]