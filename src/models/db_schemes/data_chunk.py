from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")                                                    # MongoDB uses _id as the default primary key field
    chunk_text: str = Field(..., min_length=1, description="Text content of the data chunk")
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0, description="Order of the chunk in the original document") # gt=0 means that the value must be greater than 0
    chunk_project_id: ObjectId 

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True             #########################################################
