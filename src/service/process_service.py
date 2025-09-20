from .base_service import BaseService
from .project_service import ProjectService
import os
from .document_reader_factory import DocumentReaderFactory
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ProcessService(BaseService):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_dir = ProjectService().build_project_dir(project_id)
        
    def read_file(self, file_name: str):
        loader = self.get_document_loader(file_name)
        
        if loader is None:
            return None
        
        return loader.load()

    def get_document_loader(self, file_name: str):
        file_extension = self.get_file_extension(file_name)
        file_path = os.path.join(self.project_dir, file_name)
        
        if not os.path.exists(file_path):
            return None
        
        return DocumentReaderFactory.get_document_reader(file_path, file_extension)  
    
    def get_file_extension(self, file_name: str):
        return os.path.splitext(file_name)[-1]

    
    def process_documents(self, pages: list, chunck_size: int, overlap: int):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunck_size,
            chunk_overlap = overlap,
            length_function = len
        )

        pages_text = [
            page.page_content
            for page in pages
        ]

        pages_metadata = [
            page.metadata
            for page in pages
        ]

        chunks = text_splitter.create_documents(
            pages_text,
            metadatas=pages_metadata
        )

        return chunks