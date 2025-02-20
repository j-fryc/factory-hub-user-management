from pydantic import BaseModel, field_validator, Field
from typing import Optional, Literal
from fastapi import HTTPException, Query


class SortParameters(BaseModel):
    sort_parameter: Optional[Literal['created_at', 'name', 'display_name']] = Query(None)
    sort_order: Optional[Literal['1', '-1']] = Query(None)

    @field_validator('sort_order')
    def validate_sort_order(cls, v, info):
        sort_parameter = info.data.get('sort_parameter')
        if sort_parameter and v is None:
            raise HTTPException(
                status_code=400,
                detail="If sort_parameter is provided, sort_order must also be provided as 0 or 1"
            )
        return v

    def to_query_params(self):
        if self.sort_parameter and self.sort_order is not None:
            return {'sort': f'{self.sort_parameter}:{self.sort_order}'}
        return {}


class OrganizationFields(BaseModel):
    id: str = Field(..., description="Unique organization ID")
    name: str = Field(..., description="Organization's name")
    display_name: str = Field(..., description="Organization's display name")
    branding: Optional[dict] = Field(default=None, description="Organization's logo url")


class UpdateOrganizationFields(BaseModel):
    name: Optional[str] = Field(default=None, description="Organization's name")
    display_name: Optional[str] = Field(default=None, description="Organization's display name")


class EnabledOrganizationConnections(BaseModel):
    connection_id: Literal['con_jTG5t4Fzmjd90Myb'] = 'con_jTG5t4Fzmjd90Myb'
    assign_membership_on_login: Literal[False] = False
    show_as_button: Literal[True] = True
    is_signup_enabled: Literal[False] = False


class CreateOrganizationFields(BaseModel):
    name: str = Field(..., description="Organization's name")
    display_name: str = Field(..., description="Organization's display name")
    enabled_connections: list[EnabledOrganizationConnections] = Field(..., description="List of organization's enabled connections")


class AddDeleteMembersFields(BaseModel):
    members: list[str] = Field(..., description="List of user IDs")
