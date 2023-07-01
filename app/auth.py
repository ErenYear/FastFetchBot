import secrets

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyQuery

# TODO: move to config
API_KEY_NAME = "api_key"
API_KEY = ""
TELEGRAM_API_KEY = ""

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)


def verify_key(input_key, true_key):
    if api_key_query is None or not secrets.compare_digest(input_key, true_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API Key Invalid"
        )


def verify_api_key(api_key_query: str = Security(api_key_query)):
    verify_key(api_key_query, API_KEY)


def verify_telegram_api_key(api_key_query: str = Security(api_key_query)):
    verify_key(api_key_query, TELEGRAM_API_KEY)
