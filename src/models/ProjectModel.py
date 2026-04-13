
# Creating a project model file for handling project-related database operations. (mongoDB)


from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):

        super().__init__(db_client=db_client)
        
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    # the indexing task :
    # very important to understand 
    @classmethod
    async def create_instance(cls, db_client: object):

        instance = cls(db_client=db_client)  # Create an instance of the ProjectModel class with the provided database client # call the init function
        
        await instance.init_collection()     # Initialize the collection (create it if it does not exist and set up indexes)
        
        return instance  # Return the initialized instance of the ProjectModel class



    async def init_collection(self):

        all_collections = await self.db_client.list_collection_names()  # List all collection names in the database
        
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:  # Check if the project collection exists

            self.collection = await self.db_client.create_collection(DataBaseEnum.COLLECTION_PROJECT_NAME.value)  # Create the project collection if it does not exist
            
        indexes = Project.get_indexes()  # Get the indexes defined in the Project model
            
        for index in indexes:
            await self.collection.create_index(index["key"], name=index["name"], unique=index["unique"])  # Create each index in the collection using the specified key, name, and uniqueness constraint


    async def create_project(self, project: Project):

        #project.dict()  Convert Pydantic model to dict, excluding unset fields
        # without await the code will not wait for the insert_one operation to complete, and it will return a coroutine object instead of the actual result. 
        # By using await, we ensure that the code waits for the operation to finish and retrieves the result before proceeding. 

        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True)) # by_alias means use the alias defined in the Pydantic model '_id' # exclude_unset means exclude any argument with default value # Insert the project into the collection
        
        project.id = result.inserted_id  # Set the _id field of the project to the inserted ID
        
        return project  # Return the ID of the inserted document as a string
    
    async def get_project_or_create_one(self, project_id: ObjectId):   ### str #######################################################

        reccord = await self.collection.find_one({"project_id": project_id})  # Find the project by its project_id
        if reccord is None:
            project = Project(project_id=project_id)  # Return the project as a Pydantic model
            project = await self.create_project(project)  # Create the project if it does not exist
            return project
        
        return Project(**reccord)  # Return the project if it is found   
    
    async def get_all_projects(self, page:int=1, page_size:int=10):

        # count total: 
        total_document = await self.collection.count_documents({})  # Count the total number of documents in the collection
        
        total_pages = total_document // page_size # Calculate the total number of pages
        if total_document % page_size > 0 :
            total_pages += 1
        
        # code of the collection : 
        cursor = self.collection.find().skip((page-1)*page_size).limit(page_size)  # Skip the documents for the previous pages and limit the number of documents returned to the page size
        Projects = []
        async for document in cursor:
            Projects.append(Project(**document))  # Convert each document to a Pydantic model and add it to the list
        return Projects, total_pages  # Return the list of projects and the total number of pages
    