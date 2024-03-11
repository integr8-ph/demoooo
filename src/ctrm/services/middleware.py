from fastapi import Depends, Request
from src.ctrm.helpers.exceptions import ServerError
from src.ctrm.models.logs import InboundLog, OutboundLog
from src.ctrm.services.deps import get_workbench_id
from src.logger import logger


async def log_middleware(
    request: Request,
    call_next,
    workbench_id: str = Depends(get_workbench_id),
):
    try:
        if not workbench_id:
            log_dict = {
                "path": request.url.path,
                "method": request.method,
                "headers": dict(request.headers),
                "body": await request.body(),
            }

            logger.info(log_dict, extra=log_dict)
            response = await call_next(request)

            return response

        inbound_log = InboundLog(
            workbench_id=workbench_id,
            response_status_code=202,
            response={},
            payload={},
            header=dict(request.headers),
        )

        await inbound_log.insert()

        logger.info(inbound_log.model_dump())

        response = await call_next(request)

        outbound_log = OutboundLog(
            workbench_id=workbench_id,
            response_status_code=response.status_code,
            response=dict(response.headers),
            payload={},
            header=dict(request.headers),
        )

        await outbound_log.insert()

        logger.info(outbound_log.model_dump())

        return response

    except Exception as e:
        logger.error(e)
        raise ServerError()
