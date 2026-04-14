# Creating a base data model file for common database operations and configurations. (mongoDB)
from helpers.config import get_settings, Settings

class BaseDataModel:

    def __init__(self,db_client:object,  settings: Settings = None ):
        
        self.db_client = db_client
        self.app_settings = get_settings()
