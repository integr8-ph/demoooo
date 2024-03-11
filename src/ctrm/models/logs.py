from typing import Any, Dict
from beanie import Document


class InboundLog(Document):
    workbench_id: str
    response_status_code: int
    response: Dict[str, Any] = None
    payload: Dict[str, Any] = None
    header: Dict[str, Any] = None


class OutboundLog(Document):
    workbench_id: str
    response_status_code: int
    response: Dict[str, Any] = None
    payload: Dict[str, Any] = None
    header: Dict[str, Any] = None
