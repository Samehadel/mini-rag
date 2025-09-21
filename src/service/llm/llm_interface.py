from abc import ABC, abstractmethod

class LLMInterface(ABC):
    def process_text(self, prompt: str):
        if len(prompt) > self.max_input_characters:
            prompt = prompt[:self.max_input_characters]

        return prompt
    
    @abstractmethod
    def set_generation_model(self, model_id: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float=None):
        pass

    @abstractmethod
    def generate_embedding(self, text: str, query_type: str = None):
        pass

    @abstractmethod
    def constrcut_prompt(self, prompt: str, role: str):
        pass
        