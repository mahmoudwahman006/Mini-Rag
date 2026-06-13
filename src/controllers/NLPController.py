from models import ResponseSignal as ResponseEnums
from fastapi.responses import JSONResponse
from fastapi import status
from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnums
from typing import List
import json  

class NLPController(BaseController):
    def __init__(self, vector_db_client, generation_client, embedding_client):
        super().__init__()        
    
        self.vector_db_client = vector_db_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
    
    def create_collection_name(self, project_id: str):
        return f"project_{project_id}".strip().replace("-", "_") # to avoid any issue with collection name in the vector db provider because some providers do not allow special characters in the collection name
    
    def reset_vector_db_collection(self, project: Project):

        collection_name = self.create_collection_name(project_id=project.project_id)

        if self.vector_db_client.collection_exists(collection_name=collection_name):
            return self.vector_db_client.delete_collection(collection_name=collection_name)


    async def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vector_db_client.get_collection_info(collection_name=collection_name)     ################## idet vide 16 
        
        if collection_info is None:
                return None
        
        return json.loads(
             json.dumps(collection_info, default=lambda x: x.__dict__)) # Convert non-serializable objects to dict )

    async def index_into_vector_db(self, project: Project, chunks: List[DataChunk], do_reset: bool = False):
        # 1) get collection name : 
        collection_name = self.create_collection_name(project_id=project.project_id)

        # 2) prepare the data for indexing :
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]

        vectors = [

            await self.embedding_client.embed_text(text=text,document_type = DocumentTypeEnums.DOCUMENT.value)

            for text in texts
        ]

        
        # 3) create collection if not exists 
        _ = await self.vector_db_client.create_collection(collection_name=collection_name, embedding_size=self.embedding_client.embedding_size)

        # 4) index the data into the vector db collection :
        _ = await self.vector_db_client.insert_many(
            collection_name=collection_name,
              texts=texts, 
              vectors=vectors,
                metadata=metadata,
                # record_ids=[c.chunk_id for c in chunks],
                #    batch_size=50
                )
        
        return True 
        