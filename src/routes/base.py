from fastapi import (
    FastAPI,
    APIRouter,
    Depends,

)
import os

from utils.config import (
    get_settings,  
    Settings, 

)
base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def alive(app_settigs: Settings=Depends(get_settings)):
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')

    return {
        "app_name": app_name,
        "app_version": app_version,
    }