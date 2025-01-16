from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .config import get_settings
from .users.user_manager import UserManager
from .users.routers import router as user_router

app = FastAPI()

settings = get_settings()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="fastapi_session",
    max_age=3600,
)

@app.on_event("startup")
async def startup():
    user_manager = UserManager(
        settings=get_settings(),
    )
    app.state.user_manager = user_manager

app.include_router(user_router)