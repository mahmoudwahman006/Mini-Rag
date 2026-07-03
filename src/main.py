from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
## for interface
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

## for interface

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    app.mongodb_conn = AsyncIOMotorClient(settings.MONGO_URL)
    app.db_client = app.mongodb_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(config=settings)

    vector_db_provider_factory = VectorDBProviderFactory(config=settings)

    # Generate client : 
    app.generation_client = llm_provider_factory.create(provider = settings.GENERATION_BACKEND)
    app.generation_client.set_generate_model(model_id = settings.GENERATION_MODEL_ID)

    # Embedding client :
    app.embedding_client = llm_provider_factory.create(provider = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID, embedding_size = settings.EMBEDDING_MODEL_SIZE)

    # Vector DB client :
    app.vector_db_client = vector_db_provider_factory.create(provider = settings.VECTOR_DB_BACKEND)
    app.vector_db_client.connect()





@app.on_event("shutdown")
async def shutdown_span():
    app.mongodb_conn.close()
    app.vector_db_client.disconnect()



# if function on_event is depercter we can use the lifespan context manager instead of on_event for startup and shutdown events in FastAPI. Here's how you can implement it:

## app.router.lifespan.on_startup.append(startup_span)
## app.router.lifespan.on_shutdown.append(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)