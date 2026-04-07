from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):

        super().__init__(db_client)
        
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project):

          #project.dict()  Convert Pydantic model to dict, excluding unset fields
        result = await self.collection.insert_one(project.dict())  # Insert the project into the collection
        project._id = result.inserted_id  # Set the _id field of the project to the inserted ID
        return project  # Return the ID of the inserted document as a string
    
    async def get_project_or_create_one(self, project_id: str):

        reccord = await self.collection.find_one({"project_id": project_id})  # Find the project by its project_id
        if reccord is None:
            project = Project(project_id=project_id)  # Return the project as a Pydantic model
            project = await self.create_project(project)  # Create the project if it does not exist
            return project
        
        return Project(**reccord)  # Return the project if it is found   