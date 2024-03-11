from pydantic import BaseModel, EmailStr


class Email(BaseModel):
    email: EmailStr


class NewAccount(BaseModel):
    name: str
    email: EmailStr
    link: str
    valid_hours: int = 48


class ResetPassword(BaseModel):
    token: str
