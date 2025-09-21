from model.enums.vector import VectorProviders
from helper.config import get_settings, Settings
from vector import QdrantDB
from service.base_service import BaseService

class VectorDBFactory:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.base_service = BaseService()
        self.vector_db_dir = self.base_service.get_database_path(self.settings.QDRANT_DB_PATH)
    
    def create_vector_db(self):
        vector_db_provider = self.settings.VECTOR_DB_PROVIDER

        if vector_db_provider == VectorProviders.qdrant.value:
            return QdrantDB(
                db_path=self.vector_db_dir,
                distance_method=self.settings.DISTANCE_METHOD,
            )
        