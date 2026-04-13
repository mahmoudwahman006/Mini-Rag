# vid 11

from models.db_schemes import asset
from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


class AssetModel(BaseDataModel):

    def __init__(self, db_client: object):

        super().__init__(db_client=db_client)
        
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
    
    @classmethod
    async def create_instance(cls, db_client: object):

        instance = cls(db_client=db_client)  # Create an instance of the ProjectModel class with the provided database client # call the init function
        
        await instance.init_collection()     # Initialize the collection (create it if it does not exist and set up indexes)
        
        return instance  # Return the initialized instance of the ProjectModel class



    async def init_collection(self):

        all_collections = await self.db_client.list_collection_names()  # List all collection names in the database
        
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:  # Check if the project collection exists

            self.collection = await self.db_client.create_collection(DataBaseEnum.COLLECTION_ASSET_NAME.value)  # Create the project collection if it does not exist
            
        indexes = Asset.get_indexes()  # Get the indexes defined in the Project model
            
        for index in indexes:
            await self.collection.create_index(index["key"], name=index["name"], unique=index["unique"])  # Create each index in the collection using the specified key, name, and uniqueness constraint

        
    async def create_asset(self, asset: Asset):

        #asset.dict()  Convert Pydantic model to dict, excluding unset fields
        # without await the code will not wait for the insert_one operation to complete, and it will return a coroutine object instead of the actual result. 
        # By using await, we ensure that the code waits for the operation to finish and retrieves the result before proceeding. 

        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True)) # by_alias means use the alias defined in the Pydantic model '_id' # exclude_unset means exclude any argument with default value # Insert the project into the collection
        
        asset.id = result.inserted_id  # Set the _id field of the project to the inserted ID
        
        return asset  # Return the ID of the inserted document as a string
    
    async def get_all_project_assets(self, asset_project_id: str):

        return await self.collection.find(
            {
                "asset_project_id": ObjectId(asset_project_id)
                 if  isinstance(asset_project_id, str) else asset_project_id
            }
                                          ).to_list(length=None)  # Find all assets that belong to the specified project ID and return them as a list