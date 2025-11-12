from typing import List
from fastapi import APIRouter, HTTPException, status
from models.pet_type import PetType
from models.pet_type_create import PetTypeCreate
from database.memory_db import db
from services.ninja_api import NinjaAPIService

router = APIRouter(prefix="/pet-types", tags=["pet-types"])

@router.post("", response_model=PetType, status_code=status.HTTP_201_CREATED)
def create_pet_type(pet_type_create: PetTypeCreate):
    """Create a new pet type"""
    if db.pet_type_exists(pet_type_create.type):
        raise HTTPException(
            status_code=400,
            detail={"error": "Malformed data"}
        )
    
    try:
        animal_info = NinjaAPIService.get_animal_info(pet_type_create.type)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500,
            detail={"server_error": str(e)}
        )
    
    pet_type_id = db.generate_id()

    pet_type=PetType(
        id=pet_type_id,
        type=pet_type_create.type,
        family=animal_info["family"],
        genus=animal_info["genus"],
        attributes=animal_info["attributes"],
        lifespan=animal_info["lifespan"],
        pets=[]
    )
    
    db.add_pet_type(pet_type)
    return pet_type

@router.get("", response_model=List[PetType])
def get_pet_types():
    """Get all pet types"""
    return db.get_all_pet_types()

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
    pet_type = db.get_pet_type(id)
    if not pet_type:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )

    if pet_type.pets:
        raise HTTPException(
            status_code=400,
            detail={"error": "Malformed data"}
        )

    db.delete_pet_type(id)
