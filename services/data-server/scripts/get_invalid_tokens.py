from src.database import engine
from src.models import ApiToken
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_revoked_tokens():
    with Session(engine) as session:
        tokens = session.scalars(select(ApiToken).where(ApiToken.revoked_at != None)).all()

        if not tokens:
            print("NO TOKENS")
            return

        for token in tokens:
            created = token.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')

            last_used = (token.last_used_at.strftime('%Y-%m-%d %H:%M:%S UTC') if token.last_used_at else None)

            revoked_at = (token.revoked_at.strftime('%Y-%m-%d %H:%M:%S UTC') if token.revoked_at else None)

            print(f"{token.name} | {created} | {last_used} | {revoked_at}")

if __name__ == "__main__":
    print("TOKEN_NAME | CREATED_AT | LAST_USED_AT | REVOKED_AT")
    get_revoked_tokens()