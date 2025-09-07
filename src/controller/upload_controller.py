from fastapi import APIRouter, UploadFile, status, Depends
from fastapi.responses import JSONResponse
from controller import base_controller
from service import UploadService, ProjectService, get_project_service, get_upload_service
from helper.config import Settings, get_settings
from model.enums import ResponseMessages
import aiofiles
import logging

version = "v1"
upload_file_base_route = f"{base_controller.global_base_route}/{version}"

upload_base_rotue = APIRouter(
    prefix=f"{upload_file_base_route}",
    tags=["data_v1"]
)

logger = logging.getLogger('uvicorn.error')

@upload_base_rotue.post("/upload/{application_id}")
async def upload_file(
    application_id: str, file: UploadFile, 
    project_service: ProjectService = Depends(get_project_service), 
    app_settings: Settings = Depends(get_settings),
    upload_service: UploadService = Depends(get_upload_service)):

    valid, message = upload_service.validate_uploaded_file(file)
    
    if (not valid):
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "message": message
            }
        )
    
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
        
        