from fastapi.routing import APIRouter

from ethereum_signature_database.web.api import bytes4_signature, echo, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(
    bytes4_signature.router,
    prefix="/4bytes",
    tags=["bytes4_signature"],
)
