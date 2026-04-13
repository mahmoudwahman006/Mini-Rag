from pydantic import BaseModel , Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime


class Asset(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")  
    asset_project_id: ObjectId 
    asset_type: str = Field(..., min_length=1,description="Type of the asset")
    asset_name: str = Field(..., min_length=1, description="Name of the asset")
    asset_size: int = Field(ge=0,default=None)  # gt means greater than 0 # ge means greater than or equal to 0
    asset_config: dict = Field(default=None)
    asset_pushed_at : datetime = Field(default=datetime.utcnow)
      
    class Config:        
        arbitrary_types_allowed = True
        
 
    @classmethod
    def get_indexes(cls):                   # This method is used to convert the _id field from string to ObjectId when retrieving data from the database, since MongoDB returns the _id field as a string by default, but we want to use it as an ObjectId in our application.
        return [
            {
                "key": [
                    ("asset_project_id", 1)       # 1 means ascending order, -1 means descending order
                    ],                            # Create an index on the project_id field 
                    "name": "asset_project_id_index_1",  # Name of the index
                "unique": False  
            },
            {
                "key": [
                     ("asset_project_id", 1),
                    ("asset_name", 1)       # 1 means ascending order, -1 means descending order
                    ],                      # Create an index on the asset_name field 
                    "name": "asset_project_id_name_index_1",  # Name of the index
                "unique": True              # Ensure that the project_id field is unique across all documents in the collection
            }
        ]  