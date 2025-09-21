from fastapi import APIRouter
from controller import base_controller
from schema.chat_request import ChatRequest
from service.llm import LLMFactory
version = "v1"
prefix = f"{base_controller.global_base_route}/{version}/chat"

chat_router = APIRouter(
 prefix=f"{prefix}",
 tags=["chat_v1"]
)

@chat_router.post("/")
async def chat(request: ChatRequest): 
    
    llm_provider = LLMFactory.create_generation_llm(request)
    response = llm_provider.generate_text(
        prompt=request.prompt, 
        chat_history=request.chat_history, 
        max_output_tokens=request.max_output_tokens, 
        temperature=request.temperature
    )

    return response