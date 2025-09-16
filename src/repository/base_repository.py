from helper.config import get_settings
import logging

class BaseRepository:
    def __init__(self, db_client, collection_name: str):
        self.db_client = db_client
        self.settings = get_settings()   
        self.collection_name = collection_name 
        self.logger = logging.getLogger('uvicorn.info')
        self.collection = self.db_client[collection_name]
        
    def calculate_total_pages(self, total_document_count: int, page_size: int):
        total_pages = total_document_count // page_size
        if total_document_count % page_size > 0:
            total_pages += 1
        
        return total_pages