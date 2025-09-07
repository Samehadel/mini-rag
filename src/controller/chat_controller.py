from fastapi import APIRouter
from controller import base_controller

version = "v1"
prefix = f"{base_controller.global_base_route}/{version}/chat"

chat_router = APIRouter(
 prefix=f"{prefix}",
 tags=["chat_v1"]
)

@chat_router.get("/")
async def chat(): 
    return {"message": "Hello World"}