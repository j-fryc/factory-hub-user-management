from typing import Dict

from app.auth.auth_exceptions import TokenFetcherException
from app.config import Settings

import httpx


class AuthTokenFetcher:
    def __init__(self, settings: Settings):
        self._client_id = settings.auth0_client_id
        self._client_secret = settings.auth0_client_secret
        self._auth0_url = settings.auth0_url

    def _prepare_request_data(self) -> Dict[str, any]:
        return {
            "headers": {"content-type": "application/json"},
            "json": {
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "audience": f"{self._auth0_url}/api/v2/",
                "grant_type": "client_credentials"
            },
            "api_url": f"{self._auth0_url}/oauth/token"
        }

    async def get_token(self) -> str:
        request_data = self._prepare_request_data()
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method="POST",
                    url=request_data["api_url"],
                    headers=request_data["headers"],
                    json=request_data["json"],
                )
                response.raise_for_status()
                return response.json().get("access_token")
            except httpx.HTTPStatusError as e:
                raise TokenFetcherException(f"HTTP error occurred: {e.response.status_code} {e.response.text}")
            except httpx.RequestError as e:
                raise TokenFetcherException(f"A network error occurred: {str(e)}")
