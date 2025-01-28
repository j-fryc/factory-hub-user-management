from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from app.auth.auth_token_manager import get_auth_manager_service, AuthTokenManager
from app.organizations.organization_manager import SortParameters, OrganizationManager, get_organization_manager_service
from app.organizations.schemas import CreateOrganizationFields, UpdateOrganizationFields, AddDeleteMembersFields
from app.utils.api_layer_exceptions import NotFoundException, BaseApiException, ServiceUnavailableException, \
    BadRequestException, ConflictException

router = APIRouter(prefix="/api/v1/organizations")


@router.get("/")
async def get_organizations(
        sort_parameter: SortParameters = Depends(),
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: OrganizationManager = Depends(get_organization_manager_service)
):
    try:
        organizations_data = await organization_manager_service.get_organizations(
            auth_token=await token_handler.token,
            sort_parameter=sort_parameter,
        )
        json_compatible_data = jsonable_encoder(organizations_data)
        return JSONResponse(content=json_compatible_data)
    except (NotFoundException, BadRequestException) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except (ServiceUnavailableException, BaseApiException):
        raise HTTPException(
            status_code=500,
            detail="Service unavailable"
        )


@router.post("/")
async def create_organizations(
        create_organization_parameter: CreateOrganizationFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: OrganizationManager = Depends(get_organization_manager_service)
):
    try:
        organizations_data = await organization_manager_service.create_organization(
            auth_token=await token_handler.token,
            create_organization_fields=create_organization_parameter,
        )
        json_compatible_data = jsonable_encoder(organizations_data)
        return JSONResponse(content=json_compatible_data)
    except (BadRequestException, ConflictException) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except (ServiceUnavailableException, BaseApiException):
        raise HTTPException(
            status_code=500,
            detail="Service unavailable"
        )


@router.patch("/{organization_id}")
async def update_organizations(
        organization_id: str,
        update_organization_parameter: UpdateOrganizationFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: OrganizationManager = Depends(get_organization_manager_service)
):
    try:
        organizations_data = await organization_manager_service.update_organization(
            auth_token=await token_handler.token,
            organization_id=organization_id,
            organization_updating_fields=update_organization_parameter,
        )
        json_compatible_data = jsonable_encoder(organizations_data)
        return JSONResponse(content=json_compatible_data)
    except (NotFoundException, BadRequestException) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except (ServiceUnavailableException, BaseApiException):
        raise HTTPException(
            status_code=500,
            detail="Service unavailable"
        )


@router.delete("/{organization_id}")
async def delete_organization(
        organization_id: str,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: OrganizationManager = Depends(get_organization_manager_service)
):
    try:
        await organization_manager_service.delete_organization(
            auth_token=await token_handler.token,
            organization_id=organization_id
        )
        return Response(status_code=204)
    except BadRequestException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except (ServiceUnavailableException, BaseApiException):
        raise HTTPException(
            status_code=500,
            detail="Service unavailable"
        )


@router.post("/{organization_id}/members")
async def add_users_to_organization(
        organization_id: str,
        members_list: AddDeleteMembersFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: OrganizationManager = Depends(get_organization_manager_service)
):
    try:
        await organization_manager_service.add_users_to_organization(
            auth_token=await token_handler.token,
            organization_id=organization_id,
            members_list=members_list
        )
        return Response(status_code=204)
    except (NotFoundException, BadRequestException) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except (ServiceUnavailableException, BaseApiException):
        raise HTTPException(
            status_code=500,
            detail="Service unavailable"
        )


@router.delete("/{organization_id}/members")
async def delete_users_from_organization(
        organization_id: str,
        members_list: AddDeleteMembersFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: OrganizationManager = Depends(get_organization_manager_service)
):
    try:
        await organization_manager_service.delete_users_from_organization(
            auth_token=await token_handler.token,
            organization_id=organization_id,
            members_list=members_list
        )
        return Response(status_code=204)
    except (NotFoundException, BadRequestException) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except (ServiceUnavailableException, BaseApiException):
        raise HTTPException(
            status_code=500,
            detail="Service unavailable"
        )
