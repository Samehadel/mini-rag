from pydantic import BaseModel
from typing import Optional
from model.enums.llms import LLMProvider

class ChatRequest(BaseModel):
    prompt: str
    max_output_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.1
    chat_history: Optional[list] = []    