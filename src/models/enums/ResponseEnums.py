from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    FILE_PROCESSING_SUCCESS = "file_processing_success"
    FILE_PROCESSING_FAILED = "file_processing_failed"
    NO_FILES_ERROR = "no_files_error"
    FILE_ID_ERROR = "no_file_found_with_this_ID"
    Project_NOT_FOUND = "project_not_found"
    COLLECTION_NOT_FOUND = "collection_not_found"
    INDEX_VECTOR_STORE_ERROR = "index_vector_store_error"
    INDEX_VECTOR_STORE_SUCCESS = "index_vector_store_success"
    VECTOR_DB_COLLECTION_RETRIVED_SUCCESS = "vector_db_collection_retrived_successfully"
    EMBEDDING_ERROR = "embedding_error"