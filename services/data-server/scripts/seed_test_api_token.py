import hashlib
import secrets

from sqlalchemy.orm import Session

from src.database import engine
from src.models import ApiToken


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def seed_api_token(name: str):
    token = secrets.token_urlsafe(32)
    token_hash = hash_token(token)

    with Session(engine) as session:
        api_token = ApiToken(
            token_hash=token_hash,
            name=name,
        )

        session.add(api_token)
        session.commit()

    print("API token created successfully.")
    print(f"Name: {name}")
    print(f"Token: {token}")


if __name__ == "__main__":
    seed_api_token("test")