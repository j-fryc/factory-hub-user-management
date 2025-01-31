from typing import Optional

from fastapi import Request

from app.roles.schemas import RoleFields, UserRolesFields
from app.users.schemas import SearchableUserFields, CreateUserFields, UpdateUserFields, UserFields
from app.users.users_manager_api_layer import UserManagerApiLayer
from app.config import Settings


class UserManager:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._api_layer = UserManagerApiLayer(
            auth_url=self._settings.auth0_url
        )

    async def get_users(
            self,
            auth_token: str,
            query_parameters: Optional[SearchableUserFields] = None
    ) -> list[UserFields] | list:
        users_data = await self._api_layer.make_request(
            method="GET",
            endpoint='/users',
            auth_token=auth_token,
            params=query_parameters.to_query_params() if query_parameters else {}
        )
        return [UserFields(**user_data) for user_data in users_data]

    async def delete_user(
            self,
            auth_token: str,
            user_id: str
    ) -> None:
        await self._api_layer.make_request(
            method="DELETE",
            endpoint=f'/users/{user_id}',
            auth_token=auth_token,
        )

    async def update_user(
            self,
            auth_token: str,
            user_id: str,
            updating_fields: UpdateUserFields
    ) -> UserFields:
        updated_user_data = await self._api_layer.make_request(
            method="PATCH",
            endpoint=f'/users/{user_id}',
            auth_token=auth_token,
            content=updating_fields.model_dump_json(exclude_none=True)
        )
        return UserFields(**updated_user_data)

    async def create_user(
            self,
            auth_token: str,
            user_fields: CreateUserFields
    ) -> UserFields:
        created_user_data = await self._api_layer.make_request(
            method="POST",
            endpoint='/users',
            auth_token=auth_token,
            content=user_fields.model_dump_json(exclude_none=True)
        )
        return UserFields(**created_user_data)

    async def assign_user_roles(
            self,
            auth_token: str,
            user_id: str,
            members_roles_fields: UserRolesFields
    ) -> None:
        await self._api_layer.make_request(
            method="POST",
            endpoint=f'/users/{user_id}/roles',
            auth_token=auth_token,
            content=members_roles_fields.model_dump_json(exclude_none=True)
        )

    async def delete_user_roles(
            self,
            auth_token: str,
            user_id: str,
            members_roles_fields: UserRolesFields
    ) -> None:
        await self._api_layer.make_request(
            method="DELETE",
            endpoint=f'/users/{user_id}/roles',
            auth_token=auth_token,
            content=members_roles_fields.model_dump_json(exclude_none=True)
        )

    async def get_user_roles(
            self,
            auth_token: str,
            user_id: str
    ) -> list[RoleFields] | list:
        user_roles = await self._api_layer.make_request(
            method="GET",
            endpoint=f'/users/{user_id}/roles',
            auth_token=auth_token,
        )
        return [RoleFields(**user_role) for user_role in user_roles]


def get_user_manager_service(request: Request) -> UserManager:
    return request.app.state.user_manager
