from src.database import engine
from src.models import ApiToken
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_valid_tokens():
    with Session(engine) as session:
        names = session.scalars(select(ApiToken.name).where(ApiToken.revoked_at == None)).all()

        for name in names:
            print(name)

if __name__ == "__main__":
    get_valid_tokens()