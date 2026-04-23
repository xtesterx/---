from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routers import users
from app.utils.jwt_utils import verify_access_token
from app.databaseSQL import create_db_and_tables
from contextlib import asynccontextmanager

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)

@app.get("/")
async def home(request: Request):
    session_token = request.cookies.get("session_token")
    user_name = None

    if session_token:
        user_data = verify_access_token(session_token)
        if user_data:
            user_name = user_data.get("name")

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "request": request,
            "user_name": user_name
        }
    )
