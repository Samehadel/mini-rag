from enum import Enum

class ResponseMessages(Enum):
    FILE_TYPE_NOT_ALLOWED = "File type is not allowed"
    FILE_SIZE_TOO_LARGE = "File size is too large"
    FILE_IS_VALID = "File is valid"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File upload failed"
    FILE_PROCESSED_SUCCESSFULLY = "File processed successfully"
    FILE_PROCESSED_FAILED = "File processed failed"
    FILES_NOT_FOUND = "No files found for this project"
    