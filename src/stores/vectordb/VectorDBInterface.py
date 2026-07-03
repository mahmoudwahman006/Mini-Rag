from abc import ABC, abstractmethod
from typing import List 

class VectorDBInterface(ABC):
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_existed(self, collecction_name:str) -> bool:
        pass


    @abstractmethod
    def list_all_collections(self) -> List:
        pass

    @abstractmethod
    def get_collection_info(self) -> dict:
        pass

    @abstractmethod  
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False): # (do_reset) check the existing of the collection if it existd, delet it and create again
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text: str, vector: List, metadata: dict, record_id: str):
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, texts: List, vectors: List, record_ids: List, metadata: List, batch_size: int = 50):
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit: int): # (limit) the number of results to return
        pass