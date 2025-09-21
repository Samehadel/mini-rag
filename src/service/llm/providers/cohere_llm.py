from cohere.types import embedding_type
from openai.types import embedding
from service.llm.llm_interface import LLMInterface
from helper.config import get_settings
import logging
import cohere
from model.enums.llms import CohereRoles, CohereQueryType

class CohereLLM(LLMInterface):
    def __init__(self, api_url: str = None, api_key: str = None, max_input_characters: int = 1000,
    max_output_tokens: int = 1000, temperature: float = 0.1):

        super().__init__()
        settings = get_settings()
        self.api_key = api_key if api_key else settings.COHERE_API_KEY
        self.api_url = api_url
        self.max_input_characters = max_input_characters
        self.default_max_output_tokens = max_output_tokens
        self.default_temperature = temperature
    

        self.generation_model_id = None 
        self.embedding_model_id = None
        self.embedding_size = None

        self.logger = logging.getLogger(__name__)
        self.client = cohere.Client(api_key=self.api_key)

        self.logger.info("Cohere client initialized")

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int = None,
                            temperature: float = None):
        
        if self.valid_client() is False:
            return None
        
        if self.valid_generation_model() is False:
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_max_output_tokens
        temperature = temperature if temperature else self.default_temperature
        
        response = self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )

        if self.valid_generation_response(response) is False:
            return None
        
        return response.text

    
    def valid_generation_response(self, response):
        if not response or not response.text:
            self.logger.error("Failed to generate text")
            return False
        
        return True
    
    def constrcut_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "text": self.process_text(prompt)
        }
    
    def generate_embedding(self, text: str, query_type: str):
        if self.valid_client() is False:
            return None
        
        if self.valid_embedding_model() is False:
            return None
        
        if not query_type or (query_type != CohereQueryType.QUERY.value and query_type != CohereQueryType.EMBEDDING.value):
            raise ValueError(f"Invalid query type: {query_type}")
        
        response = self.client.embed(
            model=self.embedding_model_id,
            text=[self.process_text(text)],
            input_type=query_type,
            embedding_types=["float"]
        )

        if self.valid_embedding_response(response) is False:
            return None
        
        return response.embeddings.float[0]
    
    def valid_client(self):
        if self.client is None:
            self.logger.error("Cohere client is not initialized")
            return False
        
        return True
    
    def valid_embedding_model(self):
        if self.embedding_model_id is None:
            self.logger.error("Embedding model is not set")
            return False
        
        return True
    
    def valid_generation_model(self):
        if self.generation_model_id is None:
            self.logger.error("Generation model is not set")
            return False
        
        return True
    
    def valid_embedding_response(self, response):
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Failed to generate embedding")
            return False
        
        return True