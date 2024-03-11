from fastapi import APIRouter

from src.ctrm.api.v1.endpoints import login, clients, users, forwader

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(users.router, prefix="/users", tags=["User"])
api_router.include_router(clients.router, prefix="/clients", tags=["Client"])
api_router.include_router(forwader.router, prefix="/webhook", tags=["Webhook"])
