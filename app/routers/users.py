from fastapi import APIRouter, HTTPException, Depends, Cookie
from app.service.users import register_user, login_user, get_user_from_session_token
from app.utils.jwt_utils import create_access_token, verify_access_token
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str
    phone: str
    email: str
    password: str

class LoginRequest(BaseModel):
    phone: str
    password: str

@router.post("/register")
async def register(request: RegisterRequest):
    response = await register_user(
        request.name, request.phone, request.email, request.password
    )
    return response

@router.post("/login")
async def login(request: LoginRequest):
    data = await login_user(request.phone, request.password)

    session_token = data["session_token"]

    response = JSONResponse(content={
        "message": "Авторизация прошла успешно"
    })

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return response

@router.get("/me")
async def get_user(session_token: str = Cookie(None)):
    print("SESSION:", session_token)

@router.get("/logout")
async def logout(session_token: str = Cookie(None)):
    response = JSONResponse(content={"message": "Выход из системы"})
    if session_token:
        user_data = verify_access_token(session_token)
        if user_data:
            response.delete_cookie("session_token")
    return response