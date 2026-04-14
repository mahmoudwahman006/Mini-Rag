from pydantic import BaseModel , Field, validator
from typing import Optional
from bson.objectid import ObjectId



class Project(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")  
    project_id: str = Field(...,min_length=1, description="Unique identifier for the project")


    # Custom validator to ensure project_id is alphanumeric
    @validator('project_id')
    def validate_project_id(cls, value):   # the cls present the class 
        if not value.isalnum():
            raise ValueError('project_id can only contain alphanumeric characters')
        return value
    

    # This is necessary to allow ObjectId to be used as a field type in the Pydantic model (Pydantic do not understand ObjectId by default, so we need to allow arbitrary types)
    class Config:        
        arbitrary_types_allowed = True
        populate_by_name = True             # using the alias #########################################################


    # the indexing task :     
    @classmethod
    def get_indexes(cls):                   # This method is used to convert the _id field from string to ObjectId when retrieving data from the database, since MongoDB returns the _id field as a string by default, but we want to use it as an ObjectId in our application.
        return [
            {
                "key": [
                    ("project_id", 1)       # 1 means ascending order, -1 means descending order
                    ],                      # Create an index on the project_id field 
                    "name": "project_id_index_1",  # Name of the index
                "unique": True  # Ensure that the project_id field is unique across all documents in the collection
            }
        ]  