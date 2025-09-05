from fastapi import APIRouter
from routes.base import global_base_route

version = "v1"
prefix = f"{global_base_route}/{version}/chat"

chat_router = APIRouter(
 prefix=f"{prefix}",
 tags=["chat_v1"]
)

@chat_router.get("/")
def chat(): 
    return {"message": "Hello World"}