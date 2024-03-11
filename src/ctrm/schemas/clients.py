from typing import Optional
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr, Field


class ClientCreate(BaseModel):
    workbench_id: str
    name: str
    email: EmailStr


class ClientOut(ClientCreate):
    base_url: Optional[str] = None
    api_key: Optional[str] = None


class ClientUpdate(BaseModel):
    name: str
    email: EmailStr
    password: Optional[str] = None
    base_url: Optional[str] = None


class ToggleOut(BaseModel):
    id: str = Field(..., alias="_id")
    is_active: bool


class BaseURL(BaseModel):
    base_url: str


class LoginCredentials(HTTPBasicCredentials):
    username: Optional[EmailStr] = None
    password: Optional[str] = None
