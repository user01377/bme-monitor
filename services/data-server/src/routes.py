import hashlib
import datetime
from typing import Literal
import httpx
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import ApiToken
from .database import get_db
from .schema import TelemetryOut, TelemetryCurrentOut, NodeResponseOut

api_key = APIKeyHeader(name="X-API-Key")

def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

def authenticate_user(token: str = Depends(api_key), db: Session = Depends(get_db)):
    token_hash = hash_token(token)

    api_token = db.scalar(select(ApiToken)
                          .where(ApiToken.token_hash == token_hash, ApiToken.revoked_at.is_(None)))

    if not api_token:
        raise HTTPException(status_code=401, detail="Invalid API Token.")
    
    # on successful auth, update api tokens last used field
    api_token.last_used_at = datetime.datetime.now(datetime.UTC)
    db.commit()
    
    return api_token

def handle_downstream_error(response: httpx.Response):
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise HTTPException(status_code=error.response.status_code, detail=error.response.json()["detail"])

def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

router = APIRouter(dependencies=[Depends(authenticate_user)])

@router.get("/telemetry", response_model=TelemetryOut)
async def get_telemetry(device_id: str, metric: Literal["temp", "humidity", "pressure"], range: int = 24, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get("/telemetry", params={"device_id": device_id, "metric": metric, "range": range})

    handle_downstream_error(response)

    return response.json()

@router.get("/telemetry/current", response_model=TelemetryCurrentOut)
async def get_telemetry(device_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get("/telemetry/current", params={"device_id": device_id})

    handle_downstream_error(response)

    return response.json()

@router.get("/nodes", response_model=NodeResponseOut)
async def get_telemetry(device_id: str | None = None, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get("/nodes", params={"device_id": device_id})

    handle_downstream_error(response)

    return response.json()