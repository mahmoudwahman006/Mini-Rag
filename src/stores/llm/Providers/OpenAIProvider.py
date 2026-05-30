from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging
class OpenAIProvider(LLMInterface):

    def __init__(self, api_key:str, api_url: str=None, # get the url of the api to make request deal with ollama without going to openai providers
                 
                default_input_max_characters: int = 1000,
                default_generation_max_output_tokens: int = 1000,
                default_temperature: float = 0.1):
        
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key=self.api_key, 
            api_url=self.api_url
            )
        
        self.logger = logging.getLogger(__name__)

        def set_generate_model(self, model_id: str):   # make it acceptable for changing the model id while generation
            self.generation_model_id = model_id

        def set_embedding_model(self, model_id: str, embedding_size: int): 
            self.embedding_model_id = model_id
            self.embedding_size = embedding_size


##############################

# note this fun is not in the apstract class but it is a helper function to process the text before embedding it 
# to increase the performance of the embedding model and make it more accurate | not each provider should use the function.

        def process_text(self, text:str):
            text = text.strip()
            text = text[:self.default_input_max_characters] # to make sure that the text is not too long for the embedding model
            return text

########################        
        def generate_text(self, prompt: str,chat_history:list = [], max_output_tokens: int = None, temperature: float = None):
            
            if not self.client:
                self.logger.error("OpenAI client is not initialized.")
                return None
            
            if not self.generation_model_id:
                self.logger.error("Generation model ID is not set.")
                return None
            
            chat_history.append(self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)) # to make the history of the conversation between the user and the assistant in the right format for the openai api
            
            response = self.client.chat.completions.create(
                
                model=self.generation_model_id, 
                
                messages=chat_history,
                
                max_tokens=max_output_tokens if max_output_tokens is not None else self.default_generation_max_output_tokens,
                
                temperature=temperature if temperature is not None else self.default_temperature
            )

            if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message or not response.choices[0].message.content:
                self.logger.error("Invalid response from OpenAI API for text generation.")
                return None
            
            return response.choices[0].message.content
        

        
###################        
        def embed_text(self, text: str, document_type:str=None):
            
            if not self.client:
                self.logger.error("OpenAI client is not initialized.") # kinds of logger levels: debug, info, warning, error, critical
                return None
            
            if not self.embedding_model_id:
                self.logger.error("Embedding model ID is not set.")
                return None
            
            response = self.client.embeddings.create(
                model=self.embedding_model_id, 
                input=text
            )

            if not response or not response.data or len(response.data) == 0:
                self.logger.error("Invalid response from OpenAI API for embedding.")
                return None
            return response.data[0].embedding
        
#######################
        def construct_prompt(self, prompt: str, role:str):
            return {

                "role": role,
                "content": self.process_text(prompt) # to make sure that the prompt is not too long for the generation model and to remove any extra spaces
            }  