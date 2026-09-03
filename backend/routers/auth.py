import os

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from lib.auth import AUTH_COOKIE, create_access_token, get_current_user, get_optional_current_user, hash_password, new_id, public_user, verify_password
from database import get_db
from db_models import UserRow
from models.auth import AuthResponse, LoginRequest, MessageResponse, RegisterRequest, UserPublic


router = APIRouter(prefix="/auth", tags=["auth"])


def set_auth_cookie(response: Response, user_id: str) -> None:
    response.set_cookie(
        key=AUTH_COOKIE,
        value=create_access_token(user_id),
        httponly=True,
        samesite="lax",
        secure=os.environ.get("COOKIE_SECURE", "true").lower() == "true",
        max_age=60 * 60 * 24 * 7,
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, response: Response, session: AsyncSession = Depends(get_db)):
    email = payload.email.lower()
    if await session.scalar(select(UserRow).where(UserRow.email == email)):
        raise HTTPException(status_code=409, detail="An account with that email already exists")
    user = UserRow(id=new_id(), name=payload.name.strip(), email=email, password_hash=hash_password(payload.password))
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="An account with that email already exists")
    set_auth_cookie(response, user.id)
    return AuthResponse(user=public_user(user))


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, response: Response, session: AsyncSession = Depends(get_db)):
    user = await session.scalar(select(UserRow).where(UserRow.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    set_auth_cookie(response, user.id)
    return AuthResponse(user=public_user(user))


@router.get("/me", response_model=UserPublic | None)
async def me(user: UserRow | None = Depends(get_optional_current_user)):
    return public_user(user) if user else None


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response):
    response.delete_cookie(
        AUTH_COOKIE,
        httponly=True,
        samesite="lax",
        secure=os.environ.get("COOKIE_SECURE", "true").lower() == "true",
    )
    return MessageResponse(message="Signed out")