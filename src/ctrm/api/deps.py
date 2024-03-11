from typing import Annotated
from jose.jwt import decode

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.ctrm.config.settings import get_settings
from src.ctrm.schemas.users import UserOut
from src.ctrm.services.users import get_user_by_email
from src.ctrm.models.users import User
from src.ctrm.helpers.exceptions import BadRequest

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{get_settings().API_V1_STR}/login/access-token"
)

TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep) -> User:
    payload = decode(
        token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM]
    )
    email = payload.get("sub")

    if not email:
        return None

    user = await get_user_by_email(email=email)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise BadRequest()

    return current_user


async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    user = await get_current_user(token)

    if not user.is_active:
        return None

    return UserOut(email=user.email, created_at=user.created_at)
