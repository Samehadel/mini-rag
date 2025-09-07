from fastapi import APIRouter, UploadFile, status, Depends
from fastapi.responses import JSONResponse
from service.upload_service import UploadService
from controller import base_controller
from service import UploadService, ProjectService
from helper.config import Settings, get_settings
import os
from model.enums import ResponseMessages
import aiofiles
import logging

version = "v1"
upload_file_base_route = f"{base_controller.global_base_route}/{version}"

upload_base_rotue = APIRouter(
    prefix=f"{upload_file_base_route}",
    tags=["data_v1"]
)

upload_service = UploadService()
logger = logging.getLogger('uvicorn.error')

@upload_base_rotue.post("/upload/{application_id}")
async def upload_file(application_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    valid, message = upload_service.validate_uploaded_file(file)
    
    if (not valid):
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "message": message
            }
        )
    
    project_service = ProjectService()
    file_path = project_service.build_file_dir(application_id, file.filename)
    
    try: 
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNCK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "message": ResponseMessages.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
        content = {
            "message": ResponseMessages.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_path": file_path
        }
    )
        
        