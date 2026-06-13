
from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from pymongo import InsertOne
from bson.objectid import ObjectId



class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):

        super().__init__(db_client=db_client)
        
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    # the indexing task :
    @classmethod
    async def create_instance(cls, db_client: object):

        instance = cls(db_client=db_client)  # Create an instance of the ProjectModel class with the provided database client # call the init function
        
        await instance.init_collection()  # Initialize the collection (create it if it does not exist and set up indexes)
        
        return instance  # Return the initialized instance of the ProjectModel class
    
    

    async def init_collection(self):

        all_collections = await self.db_client.list_collection_names()  # List all collection names in the database
        
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:  # Check if the chunk collection exists

            self.collection = await self.db_client.create_collection(DataBaseEnum.COLLECTION_CHUNK_NAME.value)  # Create the chunk collection if it does not exist
            
        indexes = DataChunk.get_indexes()  # Get the indexes defined in the DataChunk model
        
        for index in indexes:
            await self.collection.create_index(index["key"], name=index["name"], unique=index["unique"])  # Create each index in the collecti




    async def create_chunk(self, chunk: DataChunk):

        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True)) # by_alias means use the alias defined in the Pydantic model '_id' # exclude_unset means exclude any argument with default value 
                                                                                                  # Insert the chunk into the collection with dictionary form to insert into database
        chunk._id = result.inserted_id                                                            # Set the _id field of the chunk to the inserted ID
        return chunk                                                                              # Return the ID of the inserted document as a string
    
    async def get_chunk(self, Chunk_id: str):

        result = await self.collection.find_one({
            "_id": Chunk_id                                       # Find the chunks by their _id
            
            })  
        
        if result is None:
            return None
        
        return DataChunk(**result)                                  # Return the chunk as a Pydantic model (parrameter unpacking)
    
    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
       
        
        for i in range(0, len( chunks), batch_size):              # Insert the chunks in batches to optimize performance
            
            batch = chunks[i:i + batch_size]
            
            operations = [
                InsertOne(chunk.dict())
                  for chunk in batch
                  ]  # Create a list of InsertOne operations for the current batch of chunks, converting each chunk to a dictionary form to insert into database
        
            await self.collection.bulk_write(operations)       # Execute the bulk write operation for the current batch

        return len(chunks)


    async def delete_chunks_by_project_id(self, project_id: ObjectId):

        result = await self.collection.delete_many({"chunk_project_id": project_id})  # Delete all chunks that belong to the specified project ID
        
        return result.deleted_count  # Return the number of deleted chunks        
    
    async def delete_all_chunks(self):

        result = await self.collection.delete_many({})  # Delete all chunks in the collection
        
        return result.deleted_count  # Return the number of deleted chunks
    
    async def get_project_chunks(self, project_id: ObjectId, page_number: int = 1, page_size: int = 50):

        # pagination logic : 
        result = await self.collection.find(
            {"chunk_project_id": project_id}).skip((page_number - 1) * page_size).limit(page_size).to_list(length=None)  # Find chunks by project ID with pagination

        return [DataChunk(**chunk) for chunk in result]  # Return the list of chunks as Pydantic models (parameter unpacking)
    