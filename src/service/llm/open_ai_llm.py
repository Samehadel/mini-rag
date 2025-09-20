from service.llm.llm_interface import LLMInterface
from model.enums.llms import LLMProvider, OpenAIRoles
from helper.config import get_settings
from openai import OpenAI
import logging

class OpenAILLM(LLMInterface):
    def __init__(self, api_url: str = None, api_key: str = None, max_input_characters: int = 1000,
    max_output_tokens: int = 1000, temperature: float = 0.1):
        super().__init__()
        self.api_key = api_key if api_key else settings.OPENAI_API_KEY
        self.api_url = api_url
        self.max_input_characters = max_input_characters
        self.default_max_output_tokens = max_output_tokens
        self.default_temperature = temperature
        self.logger = logging.getLogger(__name__)
        settings = get_settings()
    

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_url
        )
    
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

        chat_history.append(
            self.constrcut_prompt(prompt, OpenAIRoles.USER.value)
        )
        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )

        if self.valid_generation_response(response) is False:
            return None

        return response.choices[0].message.content

    def process_prompt(self, prompt: str):
        if len(prompt) > self.max_input_characters:
            prompt = prompt[:self.max_input_characters]

        return prompt

    def valid_generation_response(self, response):
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Failed to generate text")
            return False
        
        return True
    
    def constrcut_prompt(self, prompt: str, role: str):
        user_processed_prompt = self.process_prompt(prompt)
        return {
            "role": role,
            "content": user_processed_prompt
        }

    def generate_embedding(self, text: str, document_type: str = None):
        
        if self.valid_client() is False:
            return None
        
        if self.valid_embedding_model() is False:
            return None
        
        response = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text
        )

        if self.valid_embedding_response(response) is False:
            return None
        
        return response.data[0].embedding
            
    def valid_client(self):
        if self.client is None:
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
        if response is None:
            self.logger.error("Failed to generate embedding")
            return False
        
        if len(response.data) == 0:
            self.logger.error("Failed to generate embedding")
            return False
        
        if len(response.data[0].embedding) != self.embedding_size:
            self.logger.error("Failed to generate embedding")
            return False
        
        return True