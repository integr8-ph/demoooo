from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from src.ctrm.schemas.clients import (
    BaseURL,
    ClientCreate,
    ClientOut,
    ClientUpdate,
    LoginCredentials,
    ToggleOut,
)
from src.ctrm.schemas.token import Token
from src.ctrm.services.auth import Inactive, create_access_token
from src.ctrm.services.clients import (
    add_client,
    authenticate_client,
    get_all_clients,
    get_client_by_id,
    reset_trigger,
    revoke_api,
    toggle,
    update_url,
    verify_client,
)

from src.ctrm.api.deps import get_current_active_superuser
from src.ctrm.helpers.exceptions import NotAuthenticated, NotFound
from src.ctrm.services.emails import send_new_account_email


router = APIRouter()

templates = Jinja2Templates(directory="src/ctrm/email-templates/build")


@router.post(
    "/token",
    response_model=Token,
    include_in_schema=True,
)
async def client_access_token(client_credentials: LoginCredentials):
    client = await authenticate_client(
        email=client_credentials.username, password=client_credentials.password
    )

    if not client:
        raise NotAuthenticated()

    if not client.is_active:
        raise Inactive()

    client_token = create_access_token(subject=client_credentials.username)

    return Token(access_token=client_token)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ClientOut,
)
async def create_client(*, client: ClientCreate, bg_tasks: BackgroundTasks):
    client_encoded = await add_client(client)
    send_new_account_email(client_encoded, bg_tasks)

    return JSONResponse(content=client_encoded, status_code=status.HTTP_201_CREATED)


@router.get("/verification", response_class=HTMLResponse)
async def client_verification(request: Request, token: str):
    client = await verify_client(token)

    if client and not client.is_active:
        client.is_active = True
        await client.save()
        return templates.TemplateResponse(
            "verification.html", {"request": request, "email": client.email}
        )


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
)
async def read_clients():
    workbenches = await get_all_clients()

    return JSONResponse(
        content=jsonable_encoder(workbenches), status_code=status.HTTP_200_OK
    )


@router.get(
    "/{client_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ClientOut,
)
async def read_client(*, client_id: str):
    client = await get_client_by_id(client_id)

    if not client:
        raise NotFound()

    return JSONResponse(
        content=jsonable_encoder(client), status_code=status.HTTP_200_OK
    )


@router.get(
    "/{client_id}/password/reset",
    dependencies=[Depends(get_current_active_superuser)],
)
async def reset_password(client_id: str):
    client_result = await reset_trigger(client_id=client_id)

    return JSONResponse(content=client_result, status_code=status.HTTP_200_OK)


@router.put(
    "/{client_id}",
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_client(*, client_id: str, client_update: ClientUpdate):
    updated_client = await update_url(client_id, client_update)

    return JSONResponse(content=updated_client, status_code=status.HTTP_200_OK)


@router.put(
    "/{client_id}/toggle-status",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ToggleOut,
    # include_in_schema=False,
)
async def update_status(client_id: str):
    """
    This is toggle the status from active to inactive (vice-versa)
    """

    client_result = await toggle(client_id=client_id)

    return JSONResponse(content=client_result, status_code=status.HTTP_200_OK)


@router.put(
    "/{client_id}/keys/revoke",
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_api_key(client_id: str):
    client_result = await revoke_api(client=client_id)

    return JSONResponse(content=client_result, status_code=status.HTTP_200_OK)


@router.put(
    "/{client_id}/base_url",
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_base_url(client_id: str, base_url: BaseURL):
    updated_client = await update_url(client_id, base_url)

    return JSONResponse(content=updated_client, status_code=status.HTTP_200_OK)
