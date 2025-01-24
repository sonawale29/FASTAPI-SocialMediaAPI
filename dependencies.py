# dependencies.py
from fastapi import Depends, Request
from utils.auth_utils import verify_access_token, extract_token_from_header


def get_current_user(request: Request) -> dict:
    """
    Dependency to get the current user based on the token in the Authorization header.
    """
    authorization = request.headers.get("Authorization")
    token = extract_token_from_header(authorization)
    user_payload = verify_access_token(token)
    return user_payload
