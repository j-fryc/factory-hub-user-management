from fastapi import Request

from app.organizations.organization_manager_api_layer import OrganizationManagerApiLayer
from app.organizations.schemas import SortParameters, OrganizationFields, UpdateOrganizationFields, \
    CreateOrganizationFields, AddDeleteMembersFields
from app.config import Settings


class OrganizationManager:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._api_layer = OrganizationManagerApiLayer(
            auth_url=self._settings.auth0_url
        )

    async def get_organizations(
            self,
            auth_token: str,
            sort_parameter: SortParameters = None,
    ) -> list[OrganizationFields] | list:
        organizations_data = await self._api_layer.make_request(
            method="GET",
            endpoint='/organizations',
            auth_token=auth_token,
            params=sort_parameter.to_query_params() if sort_parameter else {}
        )
        return [OrganizationFields(**organization_data) for organization_data in organizations_data]

    async def delete_organization(
            self,
            auth_token: str,
            organization_id: str
    ) -> None:
        await self._api_layer.make_request(
            method="DELETE",
            endpoint=f'/organizations/{organization_id}',
            auth_token=auth_token,
        )

    async def update_organization(
            self,
            auth_token: str,
            organization_id: str,
            organization_updating_fields: UpdateOrganizationFields
    ) -> OrganizationFields:
        updated_organizations_data = await self._api_layer.make_request(
            method="PATCH",
            endpoint=f'/organizations/{organization_id}',
            auth_token=auth_token,
            content=organization_updating_fields.model_dump_json(exclude_none=True)
        )
        return OrganizationFields(**updated_organizations_data)

    async def create_organization(
            self,
            auth_token: str,
            create_organization_fields: CreateOrganizationFields
    ) -> CreateOrganizationFields:
        created_organization_data = await self._api_layer.make_request(
            method="POST",
            endpoint='/organizations',
            auth_token=auth_token,
            content=create_organization_fields.model_dump_json(exclude_none=True)
        )
        return CreateOrganizationFields(**created_organization_data)

    async def add_users_to_organization(
            self,
            auth_token: str,
            organization_id: str,
            members_list: AddDeleteMembersFields
    ) -> None:
        await self._api_layer.make_request(
            method="POST",
            endpoint=f'/organizations/{organization_id}/members',
            auth_token=auth_token,
            content=members_list.model_dump_json(exclude_none=True)
        )

    async def delete_users_from_organization(
            self,
            auth_token: str,
            organization_id: str,
            members_list: AddDeleteMembersFields
    ) -> None:
        await self._api_layer.make_request(
            method="DELETE",
            endpoint=f'/organizations/{organization_id}/members',
            auth_token=auth_token,
            content=members_list.model_dump_json(exclude_none=True)
        )


def get_organization_manager_service(request: Request) -> OrganizationManager:
    return request.app.state.organization_manager
