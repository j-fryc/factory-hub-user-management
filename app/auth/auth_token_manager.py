from authlib.jose.errors import ExpiredTokenError
from fastapi import Request, HTTPException

from app.auth.auth_exceptions import TokenFetcherException, TokenVerifierException
from app.auth.auth_token_fetcher import AuthTokenFetcher
from app.auth.auth_token_verifier import AuthTokenVerifier


class AuthTokenManager:
    def __init__(
            self,
            fetcher_service: AuthTokenFetcher,
            verifier_service: AuthTokenVerifier,
            token: str = None
    ):
        self._token_fetcher_service = fetcher_service
        self._token_verifier_service = verifier_service
        self._token = token

    @property
    async def token(self) -> str:
        await self._validate_token_expiration(self._token)
        return self._token

    @classmethod
    async def create(
            cls,
            fetcher_service: AuthTokenFetcher,
            verifier_service: AuthTokenVerifier
    ) -> "AuthTokenManager":
        try:
            token = await fetcher_service.get_token()
        except TokenFetcherException:
            raise HTTPException(status_code=500)
        return cls(
            fetcher_service=fetcher_service,
            verifier_service=verifier_service,
            token=token
        )

    async def _refresh_token(self) -> None:
        try:
            self._token = await self._token_fetcher_service.get_token()
        except TokenFetcherException:
            raise HTTPException(status_code=500)

    async def _validate_token_expiration(self, token: str = None) -> None:
        if token is None:
            token = await self._refresh_token()
        try:
            await self._token_verifier_service.verify_token(token_cookie=token)
        except ExpiredTokenError:
            await self._refresh_token()
            try:
                await self._token_verifier_service.verify_token(token_cookie=self._token)
            except TokenVerifierException:
                raise HTTPException(status_code=500)
        except TokenVerifierException:
            raise HTTPException(status_code=500)


def get_auth_manager_service(request: Request) -> AuthTokenManager:
    return request.app.state.token_handler
