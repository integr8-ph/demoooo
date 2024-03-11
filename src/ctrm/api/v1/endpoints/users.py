from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.ctrm.services.users import create_user
from src.ctrm.schemas.users import UserCreate, UserOut
from src.ctrm.api.deps import get_current_active_superuser
from src.ctrm.crud.users import _user

router = APIRouter()


@router.post(
    "/signup",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserOut,
)
async def signup(user: UserCreate):
    new_user = await create_user(user_in=user)

    return JSONResponse(
        content=new_user,
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/all",
    dependencies=[Depends(get_current_active_superuser)],
)
async def read_users():
    users = await _user.get_all()

    return users
