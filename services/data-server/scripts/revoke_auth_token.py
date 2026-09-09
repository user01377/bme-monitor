import datetime
import sys

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import ApiToken

def revoke_token(name: str) -> None:
    with Session(engine) as db:
        api_token = db.scalar(
            select(ApiToken).where(ApiToken.name == name)
        )

        if api_token is None:
            print(f"Token '{name}' not found.")
            return

        if api_token.revoked_at is not None:
            print(f"Token '{name}' is already revoked.")
            return

        api_token.revoked_at = datetime.datetime.now(datetime.UTC)
        db.commit()

        print(f"Token '{name}' revoked successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m scripts.revoke_auth_token <token_name>")
        sys.exit(1)

    revoke_token(sys.argv[1])