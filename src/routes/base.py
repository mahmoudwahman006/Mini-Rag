from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, Settings # the pydantic way:

base_router = APIRouter(
    prefix="/api/v1",                             #means if i want to add a word or more in the link for all routes
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):

    '''
    # way (1) 
    app_name =  os.getenv("app_name")        ## to ask the os about the values that in the .env file and now it's in the system 
    version_name =  os.getenv("version_name")        ## to ask the os about the values that in the .env file and now it's in the system 
    
    ''' 
    '''
    # depeds replave this line 
    # the pydantic way: 
    app_settings = get_settings()
    '''


    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version,
    }
