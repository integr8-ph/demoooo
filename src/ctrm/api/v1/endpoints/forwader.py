from fastapi import APIRouter, Body, Query


from src.ctrm.services.forwader import forward_to_client, get_client_by_workbench_id
from src.ctrm.services.utils import ClientNotFound


router = APIRouter()


@router.post("/")
async def forward(aspect_workbench_id: str = Query(...), aspect_data: dict = Body(...)):
    client = await get_client_by_workbench_id(aspect_workbench_id)

    if not client:
        raise ClientNotFound()

    return await forward_to_client(client=client, data=aspect_data)
