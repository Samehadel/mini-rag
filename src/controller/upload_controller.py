from fastapi import APIRouter, UploadFile, status, Depends, Request
from fastapi.responses import JSONResponse
from controller import base_controller
from service import UploadService, ProjectService, ProcessService, get_project_service, get_upload_service
from helper.config import Settings, get_settings
from model.enums import ResponseMessages
import aiofiles
import logging
from schema import ProcessRequest
from repository import ProjectRepository, ChunckRepository, project_repository
from model.db_schema import DataChunck

version = "v1"
upload_file_base_route = f"{base_controller.global_base_route}/{version}"

upload_base_rotue = APIRouter(
    prefix=f"{upload_file_base_route}",
    tags=["data_v1"]
)

logger = logging.getLogger('uvicorn.error')

@upload_base_rotue.post("/upload/{application_id}")
async def upload_file(
    request: Request,
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
    
    file_path, file_name = project_service.build_file_dir(application_id, file.filename)
    
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

    project_repository = ProjectRepository(request.app.mongodb_client)
    project = await project_repository.find_by_application_id_or_create(application_id)
    
    return JSONResponse(
        content = {
            "message": ResponseMessages.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_path": file_path,
            "file_name": file_name,
            "project": str(project.id)
        }
    )
        
        
@upload_base_rotue.post("/process/{project_id}")
async def process_file(request: Request, project_id: str, process_request: ProcessRequest):
    process_service = ProcessService(project_id)
    pages = process_service.read_file(process_request.file_name)
    chuncks = process_service.process_documents(pages, process_request.chunck_size, process_request.overlap_size)
    
    project_repository = ProjectRepository(request.app.mongodb_client)
    project = await project_repository.find_by_application_id_or_create(project_id)
    
    if chuncks is None or len(chuncks) == 0:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "message": ResponseMessages.FILE_PROCESSED_FAILED.value
            }
        )
    

    chunck_data_list = [
        DataChunck(
            chunck_text=chunck.page_content,
            chunck_metadata=chunck.metadata,
            chunck_index=i + 1,
            chunck_application_id=project.id
        )
        for i, chunck in enumerate(chuncks)
    ]

    chunck_repository = ChunckRepository(request.app.mongodb_client)
    no_of_chuncks = await chunck_repository.saveall(chuncks=chunck_data_list)
    
    return JSONResponse(
        content = {
            "message": ResponseMessages.FILE_PROCESSED_SUCCESSFULLY.value,
            "chuncks": no_of_chuncks
        }
    )