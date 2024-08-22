from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.openapi.models import Response

from core.exceptions import RecordNotFoundError
from core.models import ImageDetail, ImageDetailCreate
from service.image_service_interface import ImageServiceInterface
from service.image_service import ImageService
from typing import List
from urllib.parse import unquote_plus
from fastapi.responses import StreamingResponse
from io import BytesIO


router = APIRouter()

@router.post("/image/", status_code=200, summary="Add a new image.")
async def add_image(prompt: ImageDetailCreate,
                    service: ImageServiceInterface = Depends(lambda: ImageService())):
    return service.create_image(prompt)

@router.get("/image/{guid}", response_model=ImageDetail, summary="Retrieve an image by GUID.")
def get_image( guid: str, service: ImageServiceInterface = Depends(lambda: ImageService())):
    try:
        return service.get_image_by_guid(guid)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")

@router.get("/image/", response_model=List[ImageDetail], summary="List all images.")
def list_images(skip: int = 0, limit: int = 10, service: ImageServiceInterface = Depends(lambda: ImageService())):
    return service.get_all_images()

@router.get("/image/{guid}/content", summary="Retrieve an image file by GUID.")
def get_image_content(guid: str, service: ImageServiceInterface = Depends(lambda: ImageService())):
    try:
        image_content = service.get_image_content(guid)
        return StreamingResponse(BytesIO(image_content), media_type="image/png")
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")

# @router.get("/Image/shekhar", summary="Retrieve an image file by GUID.")
# def get_image_content():
#     print("i am working")
#     return {"apple": "apple"}