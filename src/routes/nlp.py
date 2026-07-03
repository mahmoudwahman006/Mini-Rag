from fastapi import FastAPI, APIRouter, status, Request 
from fastapi.responses import JSONResponse
from models.db_schemes import project
from routes.schemes.nlp import PushRequest, SearchRequest
from helpers.config import get_settings, Settings  
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel 
from models import ResponseSignal as ResponseEnums
from controllers import NLPController
import logging
import json

ogger = logging.getLogger('uvicorn.error')



nlp_router = APIRouter(
    prefix="/api/v1/nlp",                                           
    tags=["api_v1", "nlp"],
)

@nlp_router.post("/index/push/{project_id}")

async def index_project(request:Request, project_id: str, push_request: PushRequest):
   
   project_model = await ProjectModel.create_instance(db_client=request.app.db_client) 

   chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

   project = await project_model.get_project_or_create_one(project_id=project_id)
 
   if not project:
     return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
          content={
             "Signal": ResponseEnums.Project_NOT_FOUND.value
             }
             )
   
   nlp_controller = NLPController(
      vector_db_client=request.app.vector_db_client,
      generation_client=request.app.generation_client,
      embedding_client=request.app.embedding_client
        )
   

   # How to get number of pages and the page size : 

   has_records = True
   page_number = 1
   inserted_records_count = 0
   idx = 0

   while has_records:
      
    page_chunks = await chunk_model.get_project_chunks(project_id=project.id, page_number=page_number)
    if len(page_chunks):
      page_number += 1
    
    elif len(page_chunks) or page_chunks == 0:
      has_records = False
      break

    chunks_ids = list(range(idx, idx + len(page_chunks)))

    idx += len(page_chunks)

    is_inserted = await nlp_controller.index_into_vector_db(project=project, chunks=page_chunks, do_reset=push_request.do_reset, chunks_ids=chunks_ids) 

    if not is_inserted:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                 "Signal": ResponseEnums.INDEX_VECTOR_STORE_ERROR.value
                 }
                 )
    inserted_records_count += len(page_chunks)

    return JSONResponse(
        content={
            "Signal": ResponseEnums.INDEX_VECTOR_STORE_SUCCESS.value,
            "InsertedRecordsCount": inserted_records_count
        }
    ) 
   

@nlp_router.get("/index/info/{project_id}")
async def get_project_indexing_status(request: Request, project_id: str):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    
    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    nlp_controller = NLPController(
        vector_db_client=request.app.vector_db_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )

    collection_info = await nlp_controller.get_vector_db_collection_info(project=project)
    
    if collection_info is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"Signal": ResponseEnums.COLLECTION_NOT_FOUND.value}
        )
    
    return JSONResponse(
       status_code=status.HTTP_200_OK,
        content={
            "Signal": ResponseEnums.VECTOR_DB_COLLECTION_RETRIVED_SUCCESS.value,
            "collection_info": collection_info
        }
    ) 


@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    
    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    nlp_controller = NLPController(
        vector_db_client=request.app.vector_db_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )

    results =  nlp_controller.search_vector_db_collection(project=project, text=search_request.text, limit=search_request.limit)   

    if not results:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"Signal": ResponseEnums.VECTOR_DB_COLLECTION_SEARCH_FAILED.value}
        )
    
    


    return results
    
