from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistaceMethodEnums
import logging
from typing import List

class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path:str, distance_method:str):

        self.clint = None
        self.db_path = db_path
        self.distance_method = None 
        
        if distance_method == DistaceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE                   ################## check the distance method in the qdrant documentation, and make sure that it's correct, and check if there is any other distance method that we can use
        elif distance_method == DistaceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT                      ################## check the distance method in the qdrant documentation, and make sure that it's correct, and check if there is any other distance method that we can use

    def connect(self):
        self.clint = QdrantClient(path=self.db_path)


    def disconnect(self):
        self.clint = None

   
    def is_collection_existed(self, collection_name:str):
        
        return self.clint.collection_exists(collection_name=collection_name)
        

    def list_all_collections(self):
        
        return self.clint.get_collections()   #.collections
    

    def get_collection_info(self, collection_name:str):

        try : 

            return self.clint.get_collection(collection_name=collection_name)
        except Exception as e:
            logging.error(f"error while getting collection info : {e}")
            return None

    def delete_collection(self, collection_name:str):

        if self.is_collection_existed(collection_name=collection_name):

            return self.clint.delete_collection(collection_name=collection_name)
        

    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        
        if do_reset == True:
            _ = self.delete_collection(collection_name=collection_name)

        if not self.is_collection_existed(collection_name=collection_name):
            _ = self.clint.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=embedding_size, distance=self.distance_method))

     
    def insert_one(self, collection_name: str, text: str, vector: List, metadata: dict, record_id: str):
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error(f"Can not insert new record to non-existed collection: {collection_name}")
            return False
        try: 
            ### client.upload_records (OLD) can't find the method in the documentaion, changed with upsert, or uplaod_points
            ### client.upsert()  It's the function that actually sends the data to Qdrant. It takes a list of PointStruct objects and writes them to the collection
            ### models.PointStruct is a data structure that represents a single point in the vector database. It contains the vector itself and any associated payload (metadata). When you create an instance of PointStruct, you provide the vector and the payload, which can include the text and any additional metadata you want to store with that point.
            ### upload_points() is a method provided by the Qdrant client that allows you to upload multiple points to a collection in a single operation. It takes the collection name and a list of PointStruct objects as arguments and writes them to the specified collection in the Qdrant database.
            """    # old one (not working)
            _ =  self.clint.upload_points(                    
                collection_name=collection_name,
                points=[
                        models.PointStruct(
                        id=[record_id],
                        vector=vector,
                        #wait_for_upload=True,                                 ## added for solve the error 
                        #input_type = "search_document",                       ## added for solve the error
                        payload={
                            "text": text,
                            "metadata": metadata })])
            """
            _ =  self.clint.upsert(                    
                collection_name=collection_name,
                points=[
                        models.PointStruct(
                        id=[record_id],
                        vector=vector,
                        #wait_for_upload=True,                                 ## added for solve the error 
                        #input_type = "search_document",                       ## added for solve the error
                        payload={
                            "text": text,
                            "metadata": metadata })])
           
        except Exception as e: 
            logging.error(f"error while inserting batch : {e}")
            return False

        
        return True
        

    def insert_many(self, collection_name: str, texts: List, vectors: List, record_ids: List, metadata: List = None, batch_size: int = 50):

        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0,len(texts)))

        for i in range(0, len(texts), batch_size):

            batch_end = i + batch_size
            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            batch_records = [

                    models.PointStruct(
                        id=batch_record_ids[x],
                        vector=batch_vectors[x],
                        #wait_for_upload=True,                                 ## added for solve the error
                        #input_type = "search_document",                       ## added for solve the error
                        payload={
                            "text": batch_texts[x],
                            "metadata": batch_metadata[x]
                     }
                 )

                for x in range(len(batch_texts))        
            ]

            try: 
                """  old way (not working)  
                _ =  self.clint.upload_points(                       ### can't find the method upload_records in the documentaion, changed with upsert, or uplaod_points
                    collection_name=collection_name,
                    records = batch_records )
                """
                _ =  self.clint.upsert(                       ### can't find the method upload_records in the documentaion, changed with upsert, or uplaod_points
                    collection_name=collection_name,
                    points = batch_records )
                  
            except Exception as e:
                logging.error(f"error while inserting batch : {e}")
                return False

            return True
            

    def search_by_vector(self, collection_name: str, vector: list, limit: int= 5):

        return self.clint.search(collection_name = collection_name, query_vector=vector, limit = limit)