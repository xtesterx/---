from app.repositories.users import create_user, get_user_by_phone, create_session_for_user, get_user_from_session
from fastapi import HTTPException
from hashlib import sha256

async def register_user(name: str, phone: str, email: str, password: str) -> dict:
    password_hash = sha256(password.encode()).hexdigest()

    existing_user = await get_user_by_phone(phone)
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь с таким номером телефона уже существует"
        )

    user_id = await create_user(name, phone, email, password_hash)
    return {"message": "Пользователь зарегистрирован", "user_id": user_id}


async def login_user(phone: str, password: str) -> dict:  
    user = await get_user_by_phone(phone)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь с таким номером телефона не найден"
        )

    stored_password_hash = user[4]
    password_hash = sha256(password.encode()).hexdigest()
    if stored_password_hash != password_hash:
        raise HTTPException(status_code=400,  detail="Неверный пароль")

    session_token = await create_session_for_user(user)

    return {
        "message": "Авторизация прошла успешно",
        "session_token": session_token
    }


async def get_user_from_session_token(session_token: str) -> dict:
    user = await get_user_from_session(session_token)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Не удалось найти пользователя по токену сессии"
        )
    return {"message": "Пользователь авторизован", "user": user}