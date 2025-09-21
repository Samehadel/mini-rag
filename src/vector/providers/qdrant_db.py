from ..vector_db_interface import VectorDBInterface
from model.enums.vector import VectorDistanceMethod
from qdrant_client import models, QdrantClient
from typing import List
import logging
from helper.config import get_settings

class QdrantDB(VectorDBInterface):
    def __init__(self, db_path: str, distance_method: str) -> None:
        self.client = None
        self.logger = logging.getLogger(__name__)
        self.db_path = db_path
        self.settings = get_settings()
        self.distance_method = None

        if distance_method is VectorDistanceMethod.DOT.value:
            self.distance_method = models.Distance.DOT
        elif distance_method is VectorDistanceMethod.COSINE.value:
            self.distance_method = models.Distance.COSINE
        else:
            self.logger.warning(f"Invalid distance method: {distance_method}")
            self.distance_method = models.Distance.DOT

    def connect(self):
        self.client = QdrantClient(
            path=self.db_path,
        )
    
    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
        
    def list_all_collections(self) -> List:
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name):
            self.client.delete_collection(collection_name=collection_name)
    
    def create_collection(self, collection_name: str, 
                                embedding_size: int = None,
                                do_reset: bool = False):
        
        if embedding_size is None:
            embedding_size = self.settings.EMBDDING_SIZE
        
        if do_reset:
            self.delete_collection(collection_name)
        
        if not self.is_collection_existed(collection_name):
            vector_params = models.VectorParams(
                size=embedding_size,
                distance=models.Distance(self.distance_method),
            )

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=vector_params,
            )    
    
    def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: dict = None, 
                         record_id: str = None):
        
        if not self.is_collection_existed(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist")
            return False
        
        self.upload_records(
            collection_name=collection_name,
            vector=vector,
            texts=text,
            metadata=metadata,
        )

        return True
        
    
    def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          record_ids: list = None, batch_size: int = 50):
        if metadata is None:
            metadata = [None] * len(texts)
        
        if record_ids is None:
            record_ids = [None] * len(texts)

        if not self.is_collection_existed(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist")
            return False

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_vectors = vectors[i:i + batch_size]
            batch_metadata = metadata[i:i + batch_size]
            batch_record_ids = record_ids[i:i + batch_size]

            batch_records = [
                self.upload_records(
                    collection_name=collection_name,
                    vector=batch_vectors[x],
                    texts=batch_texts[x],
                    metadata=batch_metadata[x],
                )
                for x in range(len(batch_texts))
            ]

            self.client.upload_records(
                collection_name=collection_name,
                records=batch_records,
            )
        
        return True
        

    def upload_records(self, collection_name: str, vector: list, texts: list, metadata: list = None):
        record = models.Record(
            vector=vector,
            payload={
                "text": texts,
                "metadata": metadata,
            },
        )
        try:
            self.client.upload_records(
                collection_name=collection_name,
                records=[record],
            )
        except Exception as e:
            self.logger.error(f"Failed to upload records: {e}")
            return False
        
        return True
    def search_by_vector(self, collection_name: str, vector: list[float], limit: int = 5):
        try:
            result = self.client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=limit,
            )

            return result
        except Exception as e:
            self.logger.error(f"Failed to search by vector: {e}")
            return None