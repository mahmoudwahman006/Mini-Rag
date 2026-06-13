from enum import Enum

class VectorDBEnums(Enum):
    QDRANT = "QDRANT"


class DistaceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"