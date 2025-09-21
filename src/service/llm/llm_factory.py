from model.enums.llms import LLMProvider
from service.llm.llm_interface import LLMInterface
from service.llm import OpenAILLM
from service.llm import CohereLLM
from schema.chat_request import ChatRequest
from helper.config import get_settings
import logging

class LLMFactory:
    
    @classmethod
    def create_generation_llm(cls, chat_request: ChatRequest) -> LLMInterface:
        settings = get_settings()
        logger = logging.getLogger(__name__)

        llm_provider = settings.LLM_PROVIDER
        logger.info(f"Creating LLM for provider: {llm_provider}")

        if llm_provider == LLMProvider.OPENAI.value:
            openai_llm = OpenAILLM(
                max_output_tokens=chat_request.max_output_tokens,
                temperature=chat_request.temperature
            )
            openai_llm.set_generation_model(settings.OPENAI_GENERATION_MODEL)
            openai_llm.set_embedding_model(settings.OPENAI_EMBEDDING_MODEL, 1536)
            return openai_llm
        
        elif llm_provider == LLMProvider.COHERE.value:
            cohere_llm = CohereLLM(
                max_output_tokens=chat_request.max_output_tokens,
                temperature=chat_request.temperature
            )
            cohere_llm.set_generation_model(settings.COHERE_GENERATION_MODEL)
            cohere_llm.set_embedding_model(settings.COHERE_EMBEDDING_MODEL, 1536)
            return cohere_llm
        else:
            raise ValueError(f"Invalid LLM provider: {llm_provider}")