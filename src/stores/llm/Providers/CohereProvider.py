from ..LLMInterface import LLMInterface
from ..LLMEnums import CohereEnums, DocumentTypeEnums
import cohere
import logging
class CohereProvider(LLMInterface):

    def __init__(self, api_key:str, 
                 
                default_input_max_characters: int = 1000,
                default_generation_max_output_tokens: int = 1000,
                default_temperature: float = 0.1):
        
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(api_key=self.api_key) 

        self.logger = logging.getLogger(__name__)

    def set_generate_model(self, model_id: str):   # make it acceptable for changing the model id while generation
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int): 
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text:str):
            text = text.strip()
            text = text[:self.default_input_max_characters] # to make sure that the text is not too long for the embedding model
            return text

################## 

    def generate_text(self, prompt: str,chat_history:list = [], max_output_tokens: int = None, temperature: float = None):
            
            if not self.client:
                self.logger.error("Cohere client is not initialized.")
                return None
            
            if not self.generation_model_id:
                self.logger.error("Generation model ID is not set.")
                return None
            
            chat_history.append(self.construct_prompt(prompt=prompt, role=CohereEnums.USER.value)) # to make the history of the conversation between the user and the assistant in the right format for the openai api
            
            ## review again to make sure :::


            response = self.client.chat(
                
                model=self.generation_model_id, 
                
                chat_history=chat_history,

                message = self.process_text(prompt),  # only the use question.
                
                max_tokens=max_output_tokens if max_output_tokens is not None else self.default_generation_max_output_tokens,
                
                temperature=temperature if temperature is not None else self.default_temperature
            )

            if not response or not response.message or not response.message.content[0] or len(response.message.content[0].text) == 0 :
                self.logger.error("Invalid response from Cohere API for text generation.")
                return None
            
            return response.message.content[0].text
    


    def embed_text(self, text: str, document_type:str=None):
            
            if not self.client:
                self.logger.error("Cohere client is not initialized.") # kinds of logger levels: debug, info, warning, error, critical
                return None
            
            if not self.embedding_model_id:
                self.logger.error("Embedding model ID is not set.")
                return None
            
            response = self.client.embed(
                 
                model=self.embedding_model_id, 
                texts=[self.process_text(text)],
                input_type=CohereEnums.DOCUMENT.value if document_type == DocumentTypeEnums.DOCUMENT.value else CohereEnums.QUERY.value, # to make the embedding model understand if the text is a document or a query to increase the performance of the embedding
                #output_dimensions=self.embedding_size,
                embedding_types=["float"]

            )

            if not response or not response.embeddings or len(response.embeddings.float_) == 0:
                self.logger.error("Invalid response from Cohere API for embedding.")
                return None
            return response.embeddings.float_[0]
        
        
#######################
    def construct_prompt(self, prompt: str, role:str):
        return {

            "role": role,
            "text": self.process_text(prompt) # to make sure that the prompt is not too long for the generation model and to remove any extra spaces
        }  
