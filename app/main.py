from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.auth.auth_token_fetcher import AuthTokenFetcher
from app.auth.auth_token_manager import AuthTokenManager
from app.auth.auth_token_verifier import AuthTokenVerifier
from app.auth.jwks_fetcher import JWKSClient
from app.config import get_settings
from app.roles.role_manager import RoleManager
from app.users.user_manager import UserManager
from app.users.routers import router as user_router
from app.organizations.routers import router as organization_router
from app.organizations.organization_manager import OrganizationManager
from app.roles.routers import router as role_router


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
        settings=settings,
    )
    organization_manager = OrganizationManager(
        settings=settings,
    )
    role_manager = RoleManager(
        settings=settings,
    )
    token_handler = await AuthTokenManager.create(
        fetcher_service=AuthTokenFetcher(settings=settings),
        verifier_service=AuthTokenVerifier(
            JWKSClient(auth_url=settings.auth0_url)
        )
    )
    app.state.user_manager = user_manager
    app.state.organization_manager = organization_manager
    app.state.role_manager = role_manager
    app.state.token_handler = token_handler

app.include_router(user_router)
app.include_router(organization_router)
app.include_router(role_router)

