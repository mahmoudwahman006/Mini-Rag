# vid 14

# Declares a method as a required contract that subclasses must implement
# Makes the parent class an abstract class (can't be instantiated directly)
# Raises a TypeError if a subclass doesn't implement all abstract methods

from abc import ABC, abstractmethod 

class LLMInterface(ABC):
    
    def __init__(self, llm):
        self.llm = llm

    @abstractmethod
    def set_generate_model(self, model_id: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass
    
    # code smill (in notes)
    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None, temperature: float = None):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str=None): # doc type for the text that will be embedded will make diffrence if it a document or a question from user // to increase the performance
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role:str): 
        pass
