from typing import Optional
from fastapi.encoders import jsonable_encoder

from src.ctrm.models.users import User
from src.ctrm.schemas.users import UserCreate, UserOut
from src.ctrm.services.auth import verify_password, hash_password
from src.ctrm.helpers.exceptions import BadRequest, Conflict, NotFound
from src.ctrm.helpers.constants import UserError
from src.ctrm.crud.users import _user


class InactiveUser(BadRequest):
    DETAIL = UserError.INACTIVE_USER


async def get_user_by_email(email: str) -> Optional[User]:
    return await _user.get(key="email", value=email)


async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(email=email)
    if not user or not verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        raise NotFound()

    return user


async def create_user(user_in: UserCreate):
    user = await get_user_by_email(user_in.email)

    if user:
        raise Conflict()

    user_in.hashed_password = hash_password(password=user_in.hashed_password)
    new_user = await _user.create(schema=user_in)
    return jsonable_encoder(
        UserOut(email=new_user.email, created_at=str(new_user.created_at))
    )
