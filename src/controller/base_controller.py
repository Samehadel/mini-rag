from fastapi import APIRouter
from helper.config import get_settings

global_base_route = "/demo/api"

app_settings = get_settings()
application_name = app_settings.APP_NAME
version = app_settings.APP_VERSION

base_router = APIRouter(
    prefix=f"{global_base_route}/v1",
    tags=["api_v1"]
)

@base_router.get("/")
async def example():
    return {"message": f"Welcome to {application_name} {version}"}


