from src.ctrm.models.clients import Client
from src.ctrm.services.utils import BaseUrlError
from src.ctrm.crud.clients import _client
from httpx import post


async def get_client_by_workbench_id(workbench_id: str):
    return await _client.get(key="workbench_id", value=workbench_id)


async def forward_to_client(client: Client, data: dict):
    if client.base_url is None:
        raise BaseUrlError()

    response = post(url=f"{client.base_url}{client.workbench_id}", data=data)
    return response.json()
