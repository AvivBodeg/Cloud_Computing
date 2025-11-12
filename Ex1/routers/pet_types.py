from fastapi import APIRouter, HTTPException, status
from models.pet_type import PetType


router = APIRouter(prefix="/pet-types", tags=["pet-types"])

@router.get("/{id}", response_model=PetType)
def get_pet_type(id: str):
    """Get a specific pet type by ID"""
    
    pet_type = db.get_pet_type(id)
    
    if not pet_type:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    
    return pet_type
