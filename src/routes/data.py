from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request 
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings                     # the pydantic way:
from controllers import DataController, ProjectController , ProcessController            # with using __init__.py
import aiofiles
import os
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk, Asset
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum
from bson.objectid import ObjectId

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",                                           #means if i want to add a word or more in the link for all routes
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")

# adding await + create instance for the project model and chunk model for calling the indexing functions :

# function end_point for uploading file
async def upload_data(request:Request, project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
        
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client) ######################### 
    project = await project_model.get_project_or_create_one(project_id=project_id)

    
    # validate the file properties
    data_controller = DataController()


    # must be a validations for any file befor uploading extensions and size  (using .env file):
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    # using try and catch to handle if there is a problem happened during the file upload process and return a signal to the user if the upload process is failed or success
    
    try:
        async with aiofiles.open(file_path, "wb") as f:                               # writing any file type with binnary mode 
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file: {e}")                              # log the error details for debugging purposes

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )
    
    # store the assets into database
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset=asset_resource)

    return JSONResponse(
            content={
                "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_id": str(asset_record.id),
                # "project_id": str(project._id) # no need for the user to know this info 
            }
        )


@data_router.post("/process/{project_id}")

# function end_point for uploading file
async def process_endpoint(project_id: str, process_request:ProcessRequest, request:Request ): ###### request
    
    #file_id= process_request.file_id                    # removeing file_id becuase it's optional vid 12
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset


    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)  ###################

    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    

    # vid 12 automate passing the file_id to the chunking process if the user did not provide it in the request body 
     
    project_file_ids = {}

    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)  

    if process_request.file_id :

        asset_record = await asset_model.get_asset_record(asset_project_id=project.id, asset_name=process_request.file_id)

        if asset_record is None:

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_ID_ERROR.value
                }
            )

        project_file_ids = {asset_record.id: asset_record.asset_name}  # if the file_id is provided in the request body we will use it for processing and ignore the other files that belong to the same project




    else:
        
        project_files = await asset_model.get_all_project_assets(asset_project_id=project.id, asset_type=AssetTypeEnum.FILE.value)

        #project_file_ids = [record.asset_name for record in project_files]  # Extract the file IDs from the asset records and convert them to strings
        
        project_file_ids = {

            record.id: record.asset_name 
                for record in project_files
            
                }
    
    
    # check 
    if len(project_file_ids) == 0:
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.NO_FILES_ERROR.value
            }
        )
    ###########

    Process_controller = ProcessController(project_id=project_id)
    
    num_records = 0
    num_files = 0

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

     ##  delete if do_reset == 1 to delete all the chunks that belong to the project before inserting the new chunks, this is useful when we want to re-process the same file with different chunk size or overlap size, or when we want to process a new file and we want to delete the old chunks that belong to the same project to avoid confusion and save storage space.
    if do_reset == 1:
        logger.info(f"deleting chunks of : {project_id}, type of project id : {type(project_id)}") ################################## 

        delete = await chunk_model.delete_chunks_by_project_id(project_id=project.id)
        
        # for deleting all chunks just remove the projet id from the function : 
        #delete = await chunk_model.delete_all_chunks()
        

        logger.info(f"deleted chunks: {delete}") ###################################
            

    for asset_id, file_id in project_file_ids.items():    # adding all the iteration of the chunking in the for loop to iterate on files                   
    
        file_content = Process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"File with ID {file_id} does not exist or is not supported for processing.")
            continue  # Skip to the next file if the current file is not found or not supported
        
        file_chuunks = Process_controller.process_file_content(
            file_content=file_content,
              file_id=file_id ,                                          
                chunk_size=chunk_size,
                 overlap_size=overlap_size
                )
        
        if file_chuunks is None or len(file_chuunks) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_PROCESSING_FAILED.value
                }
            )
        
        file_chunks_records = [

                DataChunk(

                    chunk_text=chunk.page_content,
                    chunk_metadata=chunk.metadata,
                    chunk_order= i+1,
                    chunk_project_id=project.id,
                    chunk_asset_id= asset_id  # link the chunk to the asset
                )
                for i, chunk in enumerate(file_chuunks)
            
        ]

        
    
   
    ## insert the new chunks into the database and return the number of inserted chunks in the response
        #num_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        num_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)                  # after adding the for loop we initialize num_record and adding the new values
        num_files += 1


    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESSING_SUCCESS.value,
            "Inserted_chunks": num_records,
            "Processed_files": num_files
        }
    )
