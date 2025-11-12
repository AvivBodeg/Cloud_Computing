from typing import List
from fastapi import APIRouter, HTTPException, status
from models.pet_type import PetType
from database.memory_db import db

router = APIRouter(prefix="/pet-types", tags=["pet-types"])

@router.post("", response_model=PetType, status_code=status.HTTP_201_CREATED)
def create_pet_type(pet_type: PetType):
    """Create a new pet type"""
    # Implementation would go here
    pass

@router.get("", response_model=List[PetType])
def get_pet_types():
    """Get all pet types"""
    # Implementation would go here
    pass

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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet_type(id: str):
    """Delete a specific pet type by ID"""
    # Implementation would go here
    pass
