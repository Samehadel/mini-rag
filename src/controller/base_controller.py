from fastapi import APIRouter, Depends
from helper.config import Settings, get_settings

global_base_route = "/demo/api"

app_settings: Settings = Depends(get_settings)
application_name = get_settings().APP_NAME
version = get_settings().APP_VERSION

base_router = APIRouter(
    prefix=f"{global_base_route}/v1",
    tags=["api_v1"]
)

@base_router.get("/")
async def example():
    return {"message": f"Welcome to {application_name} {version}"}


