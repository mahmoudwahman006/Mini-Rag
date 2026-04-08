
# Creating a project model file for handling project-related database operations. (mongoDB)


from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):

        super().__init__(db_client=db_client)
        
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project):

        #project.dict()  Convert Pydantic model to dict, excluding unset fields
        # without await the code will not wait for the insert_one operation to complete, and it will return a coroutine object instead of the actual result. 
        # By using await, we ensure that the code waits for the operation to finish and retrieves the result before proceeding. 

        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True)) # by_alias means use the alias defined in the Pydantic model '_id' # exclude_unset means exclude any argument with default value # Insert the project into the collection
        
        project._id = result.inserted_id  # Set the _id field of the project to the inserted ID
        
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
    