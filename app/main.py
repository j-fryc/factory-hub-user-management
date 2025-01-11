from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .config import get_settings

app = FastAPI()

settings = get_settings()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="fastapi_session",
    max_age=3600,
)
