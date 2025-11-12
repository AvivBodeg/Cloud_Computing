from fastapi import APIRouter, HTTPException, status


router = APIRouter(prefix="/pictures", tags=["pictures"])


#GET /pictures/{file-name}
@router.get("/{file_name}")
def get_picture(file_name: str):
    pass