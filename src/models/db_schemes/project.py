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
        populate_by_name = True         # using the alias #########################################################
