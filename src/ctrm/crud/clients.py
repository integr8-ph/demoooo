from typing import TypeVar

from beanie import Document

from src.ctrm.crud.base import CRUDBase
from src.ctrm.models.clients import Client

ModelType = TypeVar("ModelType", bound=Document)


class CRUDUser(CRUDBase):
    pass


_client = CRUDUser(Client)
