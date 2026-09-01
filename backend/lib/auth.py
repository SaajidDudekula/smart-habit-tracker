import os
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Cookie, HTTPException, status
from passlib.context import CryptContext

from lib.db import db
from models.auth import UserPublic


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_ALGORITHM = "HS256"
AUTH_COOKIE = "habit_access_token"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(user_id: str) -> str:
    secret = os.environ["JWT_SECRET"]
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    return jwt.encode({"sub": user_id, "exp": expires}, secret, algorithm=JWT_ALGORITHM)


async def get_current_user(token: str | None = Cookie(default=None, alias=AUTH_COOKIE)) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError
    except (jwt.PyJWTError, ValueError, KeyError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_optional_current_user(token: str | None = Cookie(default=None, alias=AUTH_COOKIE)) -> dict | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
    except (jwt.PyJWTError, KeyError):
        return None
    return await db.users.find_one({"id": user_id})


def public_user(user: dict) -> UserPublic:
    return UserPublic(id=user["id"], name=user["name"], email=user["email"])


def new_id() -> str:
    return str(uuid.uuid4())