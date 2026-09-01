from fastapi import APIRouter, Depends, HTTPException, Response, status

from lib.auth import AUTH_COOKIE, create_access_token, get_current_user, get_optional_current_user, hash_password, new_id, public_user, verify_password
from lib.db import db
from models.auth import AuthResponse, LoginRequest, MessageResponse, RegisterRequest, UserPublic


router = APIRouter(prefix="/auth", tags=["auth"])


def set_auth_cookie(response: Response, user_id: str) -> None:
    response.set_cookie(
        key=AUTH_COOKIE,
        value=create_access_token(user_id),
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24 * 7,
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, response: Response):
    email = payload.email.lower()
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=409, detail="An account with that email already exists")
    user = {"id": new_id(), "name": payload.name.strip(), "email": email, "password_hash": hash_password(payload.password)}
    await db.users.insert_one(user)
    set_auth_cookie(response, user["id"])
    return AuthResponse(user=public_user(user))


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, response: Response):
    user = await db.users.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    set_auth_cookie(response, user["id"])
    return AuthResponse(user=public_user(user))


@router.get("/me", response_model=UserPublic | None)
async def me(user: dict | None = Depends(get_optional_current_user)):
    return public_user(user) if user else None


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response):
    response.delete_cookie(AUTH_COOKIE)
    return MessageResponse(message="Signed out")