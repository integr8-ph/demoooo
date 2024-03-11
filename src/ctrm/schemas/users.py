from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str = Field(min_length=3, alias="password")
    is_superuser: bool = True


class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
