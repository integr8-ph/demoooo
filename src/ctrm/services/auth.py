from datetime import datetime, timedelta
from typing import Any, Union
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose.jwt import encode

from src.ctrm.config.settings import get_settings
from src.ctrm.helpers.constants import UserError
from src.ctrm.helpers.exceptions import BadRequest

ph = PasswordHasher()


class Inactive(BadRequest):
    DETAIL = UserError.INACTIVE_USER


def create_access_token(
    subject: Union[str, Any], expire_delta: int | None = None
) -> str:
    if expire_delta:
        expire = datetime.utcnow() + timedelta(minutes=expire_delta)
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=get_settings().ACCESS_TOKEN_EXPIRE
        )

    payload = {"sub": subject, "exp": expire}
    encoded_jwt = encode(
        payload, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password) -> bool:
    try:
        return ph.verify(hash=hashed_password, password=plain_password)
    except VerifyMismatchError:
        return


def hash_password(password: str) -> str:
    return ph.hash(password=password)
