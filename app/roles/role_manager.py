from typing import Optional

from fastapi import Request

from app.roles.roles_manager_api_layer import RoleManagerApiLayer
from app.roles.schemas import RoleFields, CreateRoleFields, UpdateRoleFields
from app.config import Settings


class RoleManager:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._api_layer = RoleManagerApiLayer(
            auth_url=self._settings.auth0_url
        )

    async def get_roles(
            self,
            auth_token: str,
            name_filter: Optional[str] = None
    ) -> list[RoleFields] | list:
        roles_data = await self._api_layer.make_request(
            method="GET",
            endpoint='/roles',
            auth_token=auth_token,
            params={'name_filter': name_filter} if name_filter else {}
        )
        return [RoleFields(**role_data) for role_data in roles_data]

    async def delete_role(
            self,
            auth_token: str,
            role_id: str
    ) -> None:
        await self._api_layer.make_request(
            method="DELETE",
            endpoint=f'/roles/{role_id}',
            auth_token=auth_token,
        )

    async def update_role(
            self,
            auth_token: str,
            role_id: str,
            updating_fields: CreateRoleFields
    ) -> RoleFields:
        updated_role_data = await self._api_layer.make_request(
            method="PATCH",
            endpoint=f'/roles/{role_id}',
            auth_token=auth_token,
            content=updating_fields.model_dump_json(exclude_none=True)
        )
        return RoleFields(**updated_role_data)

    async def create_role(
            self,
            auth_token: str,
            role_fields: UpdateRoleFields
    ) -> RoleFields:
        created_role_data = await self._api_layer.make_request(
            method="POST",
            endpoint='/roles',
            auth_token=auth_token,
            content=role_fields.model_dump_json(exclude_none=True)
        )
        return RoleFields(**created_role_data)


def get_role_manager_service(request: Request) -> RoleManager:
    return request.app.state.role_manager
