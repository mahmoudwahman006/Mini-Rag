from .BaseController import BaseController
from .ProjectController import ProjectController
import os 
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models import ProcessingEnum

class ProcessController(BaseController):
    def __init__(self   , project_id: str):
        super().__init__()  

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)


    def get_file_extension(self, file_id: str):
        
        os.path.splitext(file_id)  # split the file name and the extension
        file_extension = os.path.splitext(file_id)[-1]  # get the extension only
        return file_extension
    
    def get_file_loader(self, file_id:str):
        file_extension = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)  # get the full path of the file using the project path and the file id

        if not os.path.exists(file_path):  # check if the file exists in the project path
            return None  # return None if the file does not exist

        if file_extension == ProcessingEnum.PDF.value:  # using the value of the enum to compare with the file extension
            return PyMuPDFLoader(file_path)  # load the pdf file using the PyMuPDFLoader

        elif file_extension == ProcessingEnum.TXT.value:  # using the value of the enum to compare with the file extension    
            return TextLoader(file_path, encoding="utf-8")  # specify the encoding for text files to avoid issues with special characters

        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
    def get_file_content(self, file_id:str):
        
        loader = self.get_file_loader(file_id=file_id)
        
        if loader:
            return loader.load()  # load the content of the file using the appropriate loader
        
        return None  # return None if the file does not exist or if the file type is not supported

    def process_file_content(self, file_content:list,file_id:str, chunk_size: int=100, overlap_size: int=20):

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap_size, length_function=len)  # create an instance of the text splitter with the specified chunk size and overlap size
        
        file_content_texts = [
            rec.page_content
            for rec in file_content ]
        
        file_content_metadata = [
            rec.metadata
            for rec in file_content ]
        # to create a chunk for each page in the file and to keep the metadata of each chunk to be used later for retrieval and to keep the context of the chunk
        chuunks = text_splitter.create_documents(file_content_texts, metadatas=file_content_metadata)  # split the content into chunks using the text splitter
        
        return chuunks