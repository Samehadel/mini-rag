from fastapi import APIRouter, UploadFile
from .base import global_base_route
from controllers import UploadController

version = "v1"
prefix = f"{global_base_route}/{version}"

upload_base_rotue = APIRouter(
    prefix=f"{prefix}",
    tags=["data_v1"]
)

upload_controller = UploadController()

@upload_base_rotue.post("/upload/{application_id}")
async def upload_file(application_id: str, file: UploadFile):
    is_valid, message = upload_controller.validate_uploaded_file(file)
    
    return {
        "is_valid": is_valid,
        "message": message
    }
        