from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routers import users
from app.utils.jwt_utils import verify_access_token

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def home(request: Request):
    session_token = request.cookies.get("session_token")
    user_name = None 

    if session_token:
        user_data = verify_access_token(session_token)
        if user_data:
            user_name = user_data.get("sub")

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "request": request,
            "user_name": user_name 
        }
    )