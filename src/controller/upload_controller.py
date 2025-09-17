from fastapi import APIRouter, UploadFile, status, Depends, Request
from fastapi.responses import JSONResponse
from controller import base_controller
from service import UploadService, ProjectService, ProcessService, get_project_service, get_upload_service
from helper.config import Settings, get_settings
from model.enums import ResponseMessages
import aiofiles
import logging
from schema import ProcessRequest
from repository import ChunckRepository, BusinessRepository, AssetRepository
from model import DataChunckEntity, AssetEntity
import os
from model.enums import AssetType

version = "v1"
upload_file_base_route = f"{base_controller.global_base_route}/{version}"

upload_base_rotue = APIRouter(
    prefix=f"{upload_file_base_route}",
    tags=["data_v1"]
)

logger = logging.getLogger('uvicorn.error')

@upload_base_rotue.post("/upload/{project_id}")
async def upload_file(
    request: Request,
    project_id: str, file: UploadFile, 
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
    
    file_path, file_name = project_service.build_file_dir(project_id, file.filename)
    
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

    business_repository = await BusinessRepository.create_instance(request.app.mongodb_client)
    asset_repository = await AssetRepository.create_instance(request.app.mongodb_client)

    business_entity = await business_repository.find_by_project_id_or_create(project_id)

    asset_entity = AssetEntity(
        project_id=project_id,
        asset_type="file",
        asset_name=file_name,
        asset_size=os.path.getsize(file_path)
    )
    
    await asset_repository.save(asset_entity)
    
    return JSONResponse(
        content = {
            "message": ResponseMessages.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_path": file_path,
            "file_name": file_name,
            "project": str(business_entity.id)
        }
    )
        
        
@upload_base_rotue.post("/process/{project_id}")
async def process_file(request: Request, project_id: str, process_request: ProcessRequest):
    asset_repository = await AssetRepository.create_instance(request.app.mongodb_client)
    asset_entities = await asset_repository.find_by_project_id(project_id, AssetType.FILE.value)
    
    if asset_entities is None or len(asset_entities) == 0:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "message": ResponseMessages.FILES_NOT_FOUND.value
            }
        )
    
    process_service = ProcessService(project_id)
    business_repository = await BusinessRepository.create_instance(request.app.mongodb_client)
    business_entity = await business_repository.find_by_project_id_or_create(project_id)
    
    for asset_entity in asset_entities:
        pages = process_service.read_file(asset_entity.asset_name)
        chuncks = process_service.process_documents(pages, process_request.chunck_size, process_request.overlap_size)

        if chuncks is None or len(chuncks) == 0:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {
                    "message": ResponseMessages.FILE_PROCESSED_FAILED.value
                }
            )
    
        no_of_chuncks = await save_chuncks(chuncks, project_id, business_entity.id, request)
    
    return JSONResponse(
        content = {
            "message": ResponseMessages.FILE_PROCESSED_SUCCESSFULLY.value,
            "number_of_processed_files": len(asset_entities)
        }
    )

async def save_chuncks(chuncks: list, project_id: str, business_entity_id: str, request: Request):
    chunck_data_list = [
        DataChunckEntity(
            chunck_text=chunck.page_content,
            chunck_metadata=chunck.metadata,
            chunck_index=i + 1,
            chunck_business_entity_id=business_entity_id
            )
            for i, chunck in enumerate(chuncks)
        ]   

    chunck_repository = await ChunckRepository.create_instance(request.app.mongodb_client)
    _ = await chunck_repository.delete_chuncks_by_project_id(project_id)
    no_of_chuncks = await chunck_repository.saveall(chuncks=chunck_data_list)

    return no_of_chuncks