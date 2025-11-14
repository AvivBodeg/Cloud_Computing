from fastapi import APIRouter, HTTPException, Response

from database.memory_db import db
from services.picture import ImageService

router = APIRouter(prefix="/pictures", tags=["pictures"])

@router.get("/{file_name}")
def get_picture(file_name: str):
    """Get a picture by its file name"""

    # Check if picture exists
    image_data = db.get_picture(file_name)

    if not image_data:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"},
        )

    content_type = ImageService.get_content_type(file_name)

    return Response(content=image_data, media_type=content_type)