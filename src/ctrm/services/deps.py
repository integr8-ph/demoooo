from src.ctrm.services.clients import get_workbench_by_id


async def get_workbench_id(workbench_id: str):
    client = await get_workbench_by_id(workbench_id=workbench_id)
    print(client)
    print(client.workbench_id)
    if client.workbench_id is None:
        return None

    return client.workbench_id
