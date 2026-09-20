import pytest
import secrets
from fastapi import HTTPException
from src.routes import authenticate_user

def test_authenticate_user_valid(db_session, test_token, test_api_token):
    result = authenticate_user(test_token, db_session)

    assert result == test_api_token

def test_authenticate_user_invalid_user(db_session):
    invalid_token = secrets.token_urlsafe(32)

    with pytest.raises(HTTPException) as exc_info:
        authenticate_user(invalid_token, db_session)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid API Token."

def test_authenticate_user_revoked_token(db_session, revoked_api_token):
    with pytest.raises(HTTPException) as exc_info:
        authenticate_user(revoked_api_token, db_session)
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid API Token."