from authlib.jose import jwt, JoseError

from app.auth.auth_exceptions import TokenVerifierException
from app.auth.jwks_fetcher import JWKSClient


class AuthTokenVerifier:
    def __init__(self, jwks_client: JWKSClient):
        self._jwks_client = jwks_client

    async def verify_token(self, token_cookie: str) -> None:
        try:
            jwks = await self._jwks_client.get_jwks()
            claims = jwt.decode(
                token_cookie,
                jwks,
                claims_options={
                    'aud': {'essential': True}
                }
            )
            claims.validate()
        except JoseError as e:
            raise TokenVerifierException(f"Token verification failed: {e}")
