from datetime import datetime
from enum import Enum
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from typing import Optional


class Role(int, Enum):
    ADMIN = 1
    CLIENT = 2


class Client(Document):
    workbench_id: Indexed(str, unique=True)  # type: ignore
    name: str
    email: EmailStr
    password: Optional[str] = None
    api_key: Optional[str] = None
    version: str = "1.0"
    base_url: Optional[str] = None
    is_active: bool = False
    role: Role = Role.CLIENT
    created_at: datetime = Field(default_factory=datetime.utcnow)
