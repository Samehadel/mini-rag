from fastapi import APIRouter
import os

global_base_route = "/demo/api"
application_name = os.getenv("APP_NAME")
version = os.getenv("APP_VERSION")

base_router = APIRouter(
    prefix=f"{global_base_route}/v1",
    tags=["api_v1"]
)

@base_router.get("/")
def example():
    return {"message": f"Welcome to {application_name} v{version}"}

second_routes = APIRouter(
    prefix=f"{global_base_route}/v2",
    tags=["api_v2"]
)

@second_routes.get("/")
def example():
    return {"message": f"Welcome to {application_name} v{version}"}

