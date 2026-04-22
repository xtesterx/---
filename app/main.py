import jwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Cookie, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from contextlib import asynccontextmanager
import uvicorn
from app.databaseSQL import create_db_and_tables, create_session_for_user, get_user_from_session
from app.logger import setup_logger
from app.routers import books

SECRET_KEY = "fajkwefoaewfkawoejgvirejviesjrhibjsithjdrthbjrjkgbhgrjfkttibj"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

logger = setup_logger()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

class LoginRequest(BaseModel):
    phone: str

class VerifyCodeRequest(BaseModel):
    phone: str
    code: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    logger.debug("Приложение запущено")
    yield
    logger.debug("Приложение выключено")

app = FastAPI(lifespan=lifespan)
app.include_router(books.router)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.post("/login")
async def login(request: LoginRequest):
    phone = request.phone
    code = "1234"
    print(f"Отправка SMS на номер {phone} с кодом {code}")
    return JSONResponse(content={"message": f"SMS с кодом {code} отправлена!"})

@app.post("/verify-code")
async def verify_code(request: VerifyCodeRequest):
    phone = request.phone
    code = request.code
    if code == "1234":
        access_token = create_access_token(data={"sub": phone})
        response = JSONResponse(content={"message": "Код подтвержден!", "access_token": access_token})
        response.set_cookie(key="session_token", value=access_token, httponly=True, secure=False)  # secure=False для локальной разработки
        return response
    else:
        raise HTTPException(status_code=400, detail="Неверный код!")

@app.get("/protected")
async def protected_route(session_token: str = Cookie(None)):
    if session_token:
        user_data = verify_access_token(session_token)
        if user_data:
            return {"message": "Вы авторизованы", "user_data": user_data}
    raise HTTPException(status_code=401, detail="Не авторизован")

@app.get("/logout")
async def logout(request: Request, session_token: str = Cookie(None)):
    response = RedirectResponse(url="/")
    response.delete_cookie("session_token")
    return response

@app.get("/")
async def home(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token:
        user_data = verify_access_token(session_token)
        if user_data:
            return templates.TemplateResponse(
                request=request,
                name="home.html",
                context={"user_name": user_data.get("sub")}
            )
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user_name": None}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)