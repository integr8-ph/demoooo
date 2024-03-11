from secrets import token_urlsafe
from typing import List, Optional
from bson import ObjectId
from jose.jwt import decode
from fastapi.encoders import jsonable_encoder

from src.ctrm.config.settings import get_settings
from src.ctrm.helpers.exceptions import NotFound
from src.ctrm.schemas.clients import ClientCreate
from src.ctrm.models.clients import Client
from src.ctrm.services.auth import hash_password, verify_password
from src.ctrm.services.utils import WorkbenchConflict, requests_put
from src.ctrm.crud.clients import _client


def generate_token(rand: int = 32) -> str:
    return token_urlsafe(rand)


def generate_password() -> str:
    rand_password = generate_token(16)
    return hash_password(rand_password)


async def get_workbench_by_id(workbench_id: str) -> Optional[Client]:
    return await _client.get(key="workbench_id", value=workbench_id)


async def get_client_by_id(id: str) -> Optional[Client]:
    return await _client.get(key="_id", value=ObjectId(id))


async def get_client_by_email(email: str) -> Optional[Client]:
    return await _client.get(key="email", value=email)


async def get_all_clients() -> List[Client]:
    return await _client.get_all()


async def verify_client(token: str) -> Optional[Client]:
    payload = decode(
        token, key=get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM]
    )
    email = payload.get("email")

    if not email:
        return None

    client = await get_client_by_email(email)
    return client


async def authenticate_client(email: str, password: str) -> Optional[Client]:
    client = await get_client_by_email(email=email)

    if not client or not verify_password(
        plain_password=password, hashed_password=client.password
    ):
        raise NotFound()

    return client


async def add_client(client_in: ClientCreate):
    client = await _client.get(key="workbench_id", value=client_in.workbench_id)

    if client:
        raise WorkbenchConflict()

    client = await _client.create(client_in)

    client.password = hash_password(password="asd")
    client.api_key = generate_token()
    client = await client.save()

    return jsonable_encoder(client)


async def toggle(client_id: str):
    client = await get_client_by_id(client_id)

    if not client:
        return NotFound()

    client.is_active = not client.is_active
    await client.save()

    return jsonable_encoder(client)


async def reset_trigger(client_id: str):
    client = _client.get(key="_id", value=client_id)

    if client is None:
        return NotFound()

    url = f"{client.base_url}/password/request"

    url_response = await requests_put(url)

    return jsonable_encoder(url_response)


async def revoke_api(client_id: str):
    client = await get_client_by_id(client_id)

    if not client:
        return NotFound()

    new_api_key = generate_token()

    client.api_key = new_api_key
    updated_client = await client.save()

    return jsonable_encoder(updated_client)


async def update_url(client_id: str, url: str):
    client = await get_client_by_id(client_id)

    if not client:
        return NotFound()

    client.password = hash_password(password=client.password)
    updated_client = await _client.update(details=url, doc=client)
    return jsonable_encoder(updated_client)
