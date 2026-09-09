import hashlib
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import ApiToken
from .database import get_db
from .schema import AvgDataOut

api_key = APIKeyHeader(name="X-API-Key")


def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

def authenticate_user(token: str = Depends(api_key), db: Session = Depends(get_db)):
    token_hash = hash_token(token)

    api_token = db.scalar(select(ApiToken).where(ApiToken.token_hash == token_hash))

    if not api_token:
        raise HTTPException(status_code=401, detail="Invalid API Token.")
    
    return api_token

router = APIRouter(dependencies=[Depends(authenticate_user)])

@router.get("/get-average", response_model=AvgDataOut)
async def get_average_telemetry(request: Request):
    client = request.app.state.http_client

    response = await client.get("/telemetry/average")
    response.raise_for_status()

    return response.json()