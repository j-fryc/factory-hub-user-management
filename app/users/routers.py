from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from app.users.schemas import CreateUserFields, UpdateUserFields, SearchableUserFields
from app.users.user_manager import UserManager, get_user_manager_service
from app.utils.api_layer_exceptions import (
    BaseApiException,
    NotFoundException,
    ConflictException,
    ServiceUnavailableException,
    BadRequestException
)
from app.auth.auth_token_manager import get_auth_manager_service, AuthTokenManager

router = APIRouter(prefix="/v1/users")


@router.post("/")
async def create_user(
        user_fields: CreateUserFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        user_manager_service: UserManager = Depends(get_user_manager_service),
):
    try:
        created_user = await user_manager_service.create_user(
            auth_token=await token_handler.token,
            user_fields=user_fields
        )
        json_compatible_data = jsonable_encoder(created_user)
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
async def delete_user(
        user_id: str,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        user_manager_service: UserManager = Depends(get_user_manager_service)
):
    try:
        await user_manager_service.delete_user(
            auth_token=await token_handler.token,
            user_id=user_id
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


@router.patch("/{user_id}")
async def update_user(
        user_id: str,
        updating_fields: UpdateUserFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        user_manager_service: UserManager = Depends(get_user_manager_service)
):
    try:
        updated_user = await user_manager_service.update_user(
            auth_token=await token_handler.token,
            user_id=user_id,
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
async def get_users(
        query_parameters: SearchableUserFields = Depends(),
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        user_manager_service: UserManager = Depends(get_user_manager_service),
):
    try:
        users_data = await user_manager_service.get_users(
            auth_token=await token_handler.token,
            query_parameters=query_parameters
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
