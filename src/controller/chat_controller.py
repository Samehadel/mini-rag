from fastapi import APIRouter
from controller import base_controller
from schema.chat_request import ChatRequest
from fastapi import Request
version = "v1"
prefix = f"{base_controller.global_base_route}/{version}/chat"

chat_router = APIRouter(
 prefix=f"{prefix}",
 tags=["chat_v1"]
)

@chat_router.post("/")
async def chat(request: Request, chat_request: ChatRequest, ): 
    
    llm_provider = request.app.llm

    response = llm_provider.generate_text(
        prompt=chat_request.prompt, 
        chat_history=chat_request.chat_history, 
        max_output_tokens=chat_request.max_output_tokens, 
        temperature=chat_request.temperature
    )

    return response