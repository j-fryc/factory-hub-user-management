from collections import OrderedDict

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, Dict, List


class BaseUserModel(BaseModel):
    blocked: Optional[bool] = Field(default=None, description="Indicates if the user is blocked")
    email_verified: Optional[bool] = Field(default=None, description="Indicates if the email is verified")
    phone_number: Optional[str] = Field(default=None, description="User's phone number")
    phone_verified: Optional[bool] = Field(default=None, description="Indicates if the phone number is verified")
    given_name: Optional[str] = Field(default=None, description="User's given name")
    family_name: Optional[str] = Field(default=None, description="User's family name")
    name: Optional[str] = Field(default=None, description="User's full name")
    nickname: Optional[str] = Field(default=None, description="User's nickname")
    picture: Optional[str] = Field(default=None, description="URL to the user's profile picture")


class UserFields(BaseUserModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    connection: Optional[str] = Field(default='Username-Password-Authentication', description="Connection type for the user")
    user_metadata: Optional[Dict] = Field(default=None, description="Custom metadata for the user")
    app_metadata: Optional[Dict] = Field(default=None, description="Application-specific metadata")
    verify_email: Optional[bool] = Field(default=None, description="Should the email be verified?")
    verify_phone_number: Optional[bool] = Field(default=None, description="Should the phone number be verified?")
    client_id: Optional[str] = Field(default=None, description="Client ID associated with the user")
    username: Optional[str] = Field(default=None, description="Username for the user")


class UserUpdatingFields(UserFields):
    email: Optional[EmailStr] = Field(default=None, description="User's email address")
    password: Optional[str] = Field(default=None, description="User's password")


class SearchableFields(BaseUserModel):
    user_id: Optional[str] = Field(default=None, description="Unique user ID")
    email: Optional[EmailStr] = Field(default=None, description="User's email address")
    logins_count: Optional[int] = Field(default=None, description="Number of logins")
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[str] = Field(default=None, description="Update timestamp")
    last_login: Optional[str] = Field(default=None, description="Last login timestamp")
    last_ip: Optional[str] = Field(default=None, description="Last IP address used")
    email_domain: Optional[str] = Field(default=None, description="Domain of the email address")
    organization_id: Optional[str] = Field(default=None, description="Organization ID associated with the user")

    def to_query_params(self) -> dict:
        ordered_dict = OrderedDict()
        base_dict = self.dict(exclude_none=True)
        ordered_dict['include_fields'] = 'true'
        query_string = '&'.join(
            f"{parameter}:{value}" for parameter, value in base_dict.items()
        )
        ordered_dict['q'] = query_string
        ordered_dict['search_engine'] = 'v3'
        return ordered_dict


class Identity(BaseModel):
    connection: str = Field(..., description="The connection type for the identity")
    user_id: str = Field(..., description="The user ID for the identity")
    provider: str = Field(..., description="The provider for the identity")
    isSocial: bool = Field(..., description="Indicates whether the identity is social")


class UserManagerResponse(BaseModel):
    created_at: str = Field(..., description="Timestamp when the user was created")
    email: EmailStr = Field(..., description="User's email address")
    email_verified: bool = Field(..., description="Indicates whether the email is verified")
    identities: List[Identity] = Field(..., description="List of identities associated with the user")
    name: str = Field(..., description="Full name of the user")
    nickname: str = Field(..., description="Nickname of the user")
    picture: HttpUrl = Field(..., description="URL to the user's profile picture")
    updated_at: str = Field(..., description="Timestamp when the user was last updated")
    user_id: str = Field(..., description="Unique user ID")
