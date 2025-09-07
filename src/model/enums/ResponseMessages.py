from enum import Enum

class ResponseMessages(Enum):
    FILE_TYPE_NOT_ALLOWED = "File type is not allowed"
    FILE_SIZE_TOO_LARGE = "File size is too large"
    FILE_IS_VALID = "File is valid"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    