from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.users.schemas import UserFields, UserUpdatingFields, SearchableFields
from app.users.user_manager import UserManager, get_user_manager_service
from app.users.user_manager_exceptions import (
    UserManagerException,
    NotFoundException,
    ConflictException,
    ServiceUnavailableException,
    BadRequestException
)
from app.auth.auth_token_manager import get_auth_manager_service, AuthTokenManager

router = APIRouter(prefix="/users")


@router.post("/create")
async def create_user(
        user_fields: UserFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        user_manager_service: UserManager = Depends(get_user_manager_service),
):
    if not await token_handler.token:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )
    try:
        users = await user_manager_service.create_user(
            auth_token=await token_handler.token,
            user_fields=user_fields
        )
        return users
    except ServiceUnavailableException:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )
    except BadRequestException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except ConflictException as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
    except UserManagerException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unexpected error: {str(e)}"
        )


@router.delete("/delete")
async def delete_user(
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        user_manager_service: UserManager = Depends(get_user_manager_service)
):
    if not await token_handler.token:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )
    try:
        users = await user_manager_service.delete_user(
            auth_token=await token_handler.token,
            user_id='auth0|67859346160dd44e43f24c45'
        )
        return users
    except BadRequestException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except ServiceUnavailableException:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )
    except UserManagerException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Token verification failed: {e}",
        )


@router.patch("/update")
async def update_user(
        updating_fields: UserUpdatingFields,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        user_manager_service: UserManager = Depends(get_user_manager_service)
):
    if not await token_handler.token:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )
    try:
        users = await user_manager_service.update_user(
            auth_token=await token_handler.token,
            user_id='auth0|67859346160dd44e43f24c45',
            updating_fields=updating_fields
        )
        return users
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except ServiceUnavailableException:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )
    except BadRequestException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except UserManagerException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get("/get")
async def get_users(
        query_parameters: Optional[SearchableFields] = None,
        token_handler: AuthTokenManager = Depends(get_auth_manager_service),
        user_manager_service: UserManager = Depends(get_user_manager_service)
):
    if not await token_handler.token:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        users = await user_manager_service.get_users(
            auth_token=await token_handler.token,
            query_parameters=query_parameters
        )
        return users
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except ServiceUnavailableException:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )
    except BadRequestException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except UserManagerException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unexpected error: {str(e)}"
        )

