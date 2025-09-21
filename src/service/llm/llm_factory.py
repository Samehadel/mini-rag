from model.enums.llms import LLMProvider
from service.llm.llm_interface import LLMInterface
from service.llm import OpenAILLM
from service.llm import CohereLLM
from schema.chat_request import ChatRequest
from helper.config import get_settings
import logging

class LLMFactory:
    
    @classmethod
    def create_llm_client(cls, temperature: float, max_output_tokens: int) -> LLMInterface:
        settings = get_settings()
        logger = logging.getLogger(__name__)

        generation_provider = settings.GENERATION_PROVIDER
        generation_model_id = settings.GENERATION_MODEL_ID

        llm_client = None
        logger.info(f"Creating LLM for provider: {generation_provider}")

        # Set generation model
        if generation_provider == LLMProvider.OPENAI.value:
            llm_client = OpenAILLM(
                max_output_tokens=max_output_tokens,
                temperature=temperature
            )
            llm_client.set_generation_model(generation_model_id)
        
        elif generation_provider == LLMProvider.COHERE.value:
            llm_client = CohereLLM(
                max_output_tokens=max_output_tokens,
                temperature=temperature
            )
            llm_client.set_generation_model(generation_model_id)
        else:
            raise ValueError(f"Invalid LLM provider: {generation_provider}")

        return llm_client

    @classmethod
    def create_embedding_client(cls, embedding_size: int) -> LLMInterface:
        settings = get_settings()
        logger = logging.getLogger(__name__)

        embedding_provider = settings.EMBEDDING_PROVIDER
        embedding_model_id = settings.EMBEDDING_MODEL_ID
        embedding_size = settings.EMBDDING_SIZE

        embedding_client = None
        logger.info(f"Creating LLM for provider: {embedding_provider}")

        # Set embedding model
        if embedding_provider == LLMProvider.OPENAI.value:
            embedding_client = OpenAILLM(
                max_output_tokens=embedding_size,
                temperature=0.7
            )
            embedding_client.set_embedding_model(embedding_model_id, embedding_size)
        elif embedding_provider == LLMProvider.COHERE.value:
            embedding_client = CohereLLM(
                max_output_tokens=embedding_size,
                temperature=0.7
            )
            embedding_client.set_embedding_model(embedding_model_id, embedding_size)
        else:
            raise ValueError(f"Invalid LLM provider: {embedding_provider}")
        
        return embedding_client