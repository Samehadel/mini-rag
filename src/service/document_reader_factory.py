from model import FileType
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
import logging


logger = logging.getLogger(__name__) 

class DocumentReaderFactory:
    @staticmethod
    def get_document_reader(file_path: str, file_extension: str):
        logger.info(f"Processing file: {file_path}, extension: {file_extension}")
        file_extension = file_extension.lower().lstrip(".")

        if file_extension == FileType.PDF.value:
            return PyMuPDFLoader(file_path)
        elif file_extension == FileType.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")