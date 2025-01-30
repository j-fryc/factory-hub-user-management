from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from app.roles.role_manager import RoleManager, get_role_manager_service
from app.roles.schemas import CreateRoleFields, UpdateRoleFields, OrganizationUserRolesFields
from app.utils.api_layer_exceptions import (
    BaseApiException,
    NotFoundException,
    ConflictException,
    ServiceUnavailableException,
    BadRequestException
)
from app.auth.auth_token_manager import get_auth_manager_service, AuthTokenManager

router = APIRouter(prefix="/api/v1/roles")


@router.post("/")
async def create_role(
        role_fields: CreateRoleFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        role_manager_service: RoleManager = Depends(get_role_manager_service)
):
    try:
        created_role = await role_manager_service.create_role(
            auth_token=await token_handler.token,
            role_fields=role_fields
        )
        json_compatible_data = jsonable_encoder(created_role)
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


@router.delete("/{user_id}")
async def delete_role(
        role_id: str,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        role_manager_service: RoleManager = Depends(get_role_manager_service)
):
    try:
        await role_manager_service.delete_role(
            auth_token=await token_handler.token,
            role_id=role_id
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


@router.patch("/{role_id}")
async def update_role(
        role_id: str,
        updating_fields: UpdateRoleFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        role_manager_service: RoleManager = Depends(get_role_manager_service)
):
    try:
        updated_user = await role_manager_service.update_role(
            auth_token=await token_handler.token,
            role_id=role_id,
            updating_fields=updating_fields
        )
        json_compatible_data = jsonable_encoder(updated_user)
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


@router.get("/")
async def get_roles(
        q: str | None = None,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        role_manager_service: RoleManager = Depends(get_role_manager_service)
):
    try:
        users_data = await role_manager_service.get_roles(
            auth_token=await token_handler.token,
            name_filter=q
        )
        json_compatible_data = jsonable_encoder(users_data)
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


@router.get("/{organization_id}/members/{user_id}")
async def get_organization_roles(
        organization_id: str,
        user_id: str,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: RoleManager = Depends(get_role_manager_service)
):
    try:
        organizations_roles_data = await organization_manager_service.get_user_roles_in_organization(
            auth_token=await token_handler.token,
            organization_id=organization_id,
            user_id=user_id
        )
        json_compatible_data = jsonable_encoder(organizations_roles_data)
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


@router.delete("/{organization_id}/members/{user_id}")
async def delete_users_roles_from_organization_member(
        organization_id: str,
        user_id: str,
        organization_user_fields: OrganizationUserRolesFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: RoleManager = Depends(get_role_manager_service)
):
    try:
        await organization_manager_service.delete_user_roles_in_organization(
            auth_token=await token_handler.token,
            organization_id=organization_id,
            user_id=user_id,
            members_roles_fields=organization_user_fields
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


@router.post("/{organization_id}/members/{user_id}")
async def assign_user_roles_in_organization(
        organization_id: str,
        user_id: str,
        organization_user_fields: OrganizationUserRolesFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        organization_manager_service: RoleManager = Depends(get_role_manager_service)
):
    try:
        await organization_manager_service.assign_user_roles_in_organization(
            auth_token=await token_handler.token,
            organization_id=organization_id,
            user_id=user_id,
            members_roles_fields=organization_user_fields
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
