from typing import Optional, Dict, Any, Union

import httpx

from app.users.user_manager_exceptions import (
    UserManagerException,
    NotFoundException,
    ConflictException,
    ServiceUnavailableException,
    BadRequestException
)


class UserManagerApiLayer:
    def __init__(self, api_url: str):
        self._api_url = api_url
        self._base_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self._exceptions_dict = {
            404: NotFoundException,
            409: ConflictException,
            400: BadRequestException,
            503: ServiceUnavailableException,
            'default': UserManagerException
        }

    def _get_headers(self, auth_token: str) -> dict:
        headers = self._base_headers.copy()
        headers['Authorization'] = f'Bearer {auth_token}'
        return headers

    async def make_request(
            self,
            method: str,
            endpoint: str,
            auth_token: str,
            params: Optional[Dict[str, Any]] = None,
            content: Optional[str] = None,
    ) -> Union[httpx.Response, list]:
        url = f"{self._api_url}{endpoint}"
        headers = self._get_headers(auth_token)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    content=content,
                )
                response.raise_for_status()
                if response.status_code == '204':
                    return []
                return response.json()
            except httpx.RequestError as e:
                raise self._exceptions_dict['default'](e)
            except httpx.HTTPStatusError as e:
                exception_to_rise = self._exceptions_dict.get(e.response.status_code)
                if exception_to_rise:
                    raise exception_to_rise(e)
                raise self._exceptions_dict['default'](e)
