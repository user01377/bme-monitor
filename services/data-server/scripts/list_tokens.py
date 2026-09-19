from src.database import engine
from src.models import ApiToken
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_token_names():
    with Session(engine) as session:
        names = session.scalars(select(ApiToken.name)).all()

        for name in names:
            print(name)

if __name__ == "__main__":
    get_token_names()