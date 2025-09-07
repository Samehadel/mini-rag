from .base_service import BaseService
from fastapi import UploadFile
from model import ResponseMessages

class UploadService(BaseService):
    def __init__(self):
        super().__init__()
        self.size_limit = 1024 * 1024 * self.settings.FILE_MAX_SIZE_MB
        self.allowed_types = self.settings.FILE_ALLOWED_TYPES

    def validate_uploaded_file(self, file: UploadFile):
        if (file.content_type not in self.allowed_types):
            return False, ResponseMessages.FILE_TYPE_NOT_ALLOWED.value
        
        if (file.size > self.size_limit):
            return False, ResponseMessages.FILE_SIZE_TOO_LARGE.value
        
        return True, ResponseMessages.FILE_IS_VALID.value
            
def get_upload_service():
    return UploadService()