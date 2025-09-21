from enum import Enum

class LLMProvider(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    ANTHROPIC = "anthropic"

class OpenAIRoles(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class CohereRoles(Enum):
    USER = "USER"
    ASSISTANT = "CHATBOT"
    SYSTEM = "SYSTEM"

class CohereQueryType(Enum):
    QUERY = "search_query"
    DOCUMENT = "search_document"