from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
def get_health():
    return {"status": "ok"}