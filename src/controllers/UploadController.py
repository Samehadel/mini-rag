from .BaseController import BaseController
from fastapi import UploadFile

class UploadController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_limit = 1024 * 1024 * self.settings.FILE_MAX_SIZE_MB
        self.allowed_types = self.settings.FILE_ALLOWED_TYPES

    def validate_uploaded_file(self, file: UploadFile):
        if (file.content_type not in self.allowed_types):
            return False
        
        if (file.size > self.size_limit):
            return False
        
        return True
            