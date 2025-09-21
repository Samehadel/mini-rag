from enum import Enum

class VectorProviders(Enum):
    qdrant = "qdrant"
    postgres = "pgvector"

class VectorDistanceMethod(Enum):
    DOT = "dot"
    COSINE = "cosine"