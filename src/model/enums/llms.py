from enum import Enum


class LLMProvider(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    ANTHROPIC = "anthropic"

class OpenAIRoles(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    