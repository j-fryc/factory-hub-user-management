from typing import Dict

import httpx

from app.auth.auth_exceptions import JWKSClientException


class JWKSClient:
    def __init__(self, auth_url: str):
        self._jwks_url = f"{auth_url}/.well-known/jwks.json"

    async def get_jwks(self) -> Dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self._jwks_url)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            raise JWKSClientException(f"Error fetching JWKS: {e}")
        except httpx.HTTPStatusError as e:
            raise JWKSClientException(f"JWKS request failed with status {e.response.status_code}")