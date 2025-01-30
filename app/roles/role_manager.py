from typing import Optional

from fastapi import Request

from app.roles.roles_manager_api_layer import RoleManagerApiLayer
from app.roles.schemas import RoleFields, CreateRoleFields, UpdateRoleFields, OrganizationUserRolesFields
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
            updating_fields: UpdateRoleFields
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
            role_fields: CreateRoleFields
    ) -> RoleFields:
        created_role_data = await self._api_layer.make_request(
            method="POST",
            endpoint='/roles',
            auth_token=auth_token,
            content=role_fields.model_dump_json(exclude_none=True)
        )
        return RoleFields(**created_role_data)

    async def assign_user_roles_in_organization(
            self,
            auth_token: str,
            organization_id: str,
            user_id: str,
            members_roles_fields: OrganizationUserRolesFields
    ) -> None:
        await self._api_layer.make_request(
            method="POST",
            endpoint=f'/organizations/{organization_id}/members/{user_id}/roles',
            auth_token=auth_token,
            content=members_roles_fields.model_dump_json(exclude_none=True)
        )

    async def delete_user_roles_in_organization(
            self,
            auth_token: str,
            organization_id: str,
            user_id: str,
            members_roles_fields: OrganizationUserRolesFields
    ) -> None:
        await self._api_layer.make_request(
            method="DELETE",
            endpoint=f'/organizations/{organization_id}/members/{user_id}/roles',
            auth_token=auth_token,
            content=members_roles_fields.model_dump_json(exclude_none=True)
        )

    async def get_user_roles_in_organization(
            self,
            auth_token: str,
            organization_id: str,
            user_id: str
    ) -> list[RoleFields] | list:
        organization_user_roles = await self._api_layer.make_request(
            method="GET",
            endpoint=f'/organizations/{organization_id}/members/{user_id}/roles',
            auth_token=auth_token,
        )
        return [RoleFields(**organization_user_role) for organization_user_role in organization_user_roles]


def get_role_manager_service(request: Request) -> RoleManager:
    return request.app.state.role_manager
