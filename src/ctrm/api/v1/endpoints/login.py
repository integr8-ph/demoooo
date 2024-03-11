from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.ctrm.services.auth import Inactive, create_access_token
from src.ctrm.schemas.token import Token
from src.ctrm.config.settings import get_settings
from src.ctrm.services.users import authenticate_user
from src.ctrm.api.deps import get_current_active_user
from src.ctrm.schemas.users import UserOut
from src.ctrm.helpers.exceptions import NotAuthenticated

router = APIRouter()


@router.post(
    "/login/access-token",
    include_in_schema=False,
)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise NotAuthenticated()

    if not user.is_active:
        raise Inactive()

    access_token_expire = get_settings().ACCESS_TOKEN_EXPIRE

    token = create_access_token(subject=user.email, expire_delta=access_token_expire)

    return Token(access_token=token)


@router.get(
    "/me",
    include_in_schema=False,
)
async def dashboard(user: UserOut = Depends(get_current_active_user)):
    return user
