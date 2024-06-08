from fastapi import (
    FastAPI,
    APIRouter,
    Depends,
    UploadFile,
    status, 
)
from fastapi.responses import JSONResponse
import os
from models import ResponseSignal

from utils.config import (
    get_settings,  
    Settings, 
)
from controllers import (
    DataController,
    ProjectController,    
)
import aiofiles
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)
import logging


logger = logging.getLogger('uvicorn.error')
@data_router.post("/upload/{project_id}")
async def upload(
    project_id: str, file: UploadFile, 
    app_settigs: Settings=Depends(get_settings)
):
    data_controller = DataController()
    # validate the file properties 
    is_valid, signal = data_controller.validate_upload_file(file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": signal
            }
        )
    project_dir_path = ProjectController().get_project_path(project_id)
    file_path, _ = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    try:
            
        async with aiofiles.open(file_path, 'wb') as f: 
            while chunk := await file.read(app_settigs.FILE_DEFAULT_CHUNK_SIZE): 
                await f.write(chunk)
    except Exception as e:
        logger.error(f'error while uploading file{e}')
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value
        }
    )