## Better way to deal with .env file and make an auto validation
# Better than load_env in the main.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    ## will validate the data in .env file :

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGO_URL : str
    MONGODB_DATABASE: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
 