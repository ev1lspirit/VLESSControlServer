from uuid import UUID
from pydantic import BaseModel, EmailStr


class AddNewUserToConfigurationBody(BaseModel):
    uuid: UUID
    UserId: int
    email: EmailStr
    flow: str


class AddClientToConfigBody(BaseModel):
    id: str
    email: EmailStr


class DeleteClientFromConfigBody(BaseModel):
    id: str


class AddNewUserToConfigurationResponse(BaseModel):
    uuid: UUID
    message: str


class GetConnectionLinkBody(BaseModel):
    id: str
