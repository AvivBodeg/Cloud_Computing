import re
from fastapi import APIRouter, HTTPException, status
from models.pet_create import PetCreate
from models.pet import Pet
from database.memory_db import db
from services.picture import ImageService
from typing import List, Optional
from datetime import datetime


router = APIRouter(prefix="/pet-types/{id}/pets", tags=["pets"])

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string in DD-MM-YYYY format"""
    pattern = r"^\d{2}-\d{2}-\d{4}$" # DD-MM-YYYY
    if re.match(pattern, date_str):
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            return None
    return None

@router.post("", response_model=Pet, status_code=status.HTTP_201_CREATED)
def create_pet(id: str, pet_create: PetCreate):
    """Create a new pet for a pet type"""
    
    # Check if pet type exists
    pet_type = db.get_pet_type(id)
    if not pet_type:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    
    # Check if pet already exists
    if db.pet_exists(id, pet_create.name):
        raise HTTPException(
            status_code=400,
            detail={"error": "Malformed data"}
        )
    
    birthdate = pet_create.birthdate or "NA"
    picture = "NA"

    # First create the pet with default picture
    try:
        pet = Pet(
            name=pet_create.name,
            birthdate=birthdate,
            picture=picture
        )
    except Exception as e:
        print("Error creating pet object:", e)
        raise HTTPException(
            status_code=400,
            detail={"error": "Malformed data"}
        )

    # Add the pet to the database first
    success = db.add_pet(id, pet)
    if not success:
        print("Failed to add pet to database")
        raise HTTPException(
            status_code=400,
            detail={"error": "Malformed data"}
        )

    # Now handle picture download after pet is safely stored
    if pet_create.picture_url and pet_create.picture_url != "NA":
        try:
            filename, image_data = ImageService.download_image(
                pet_create.picture_url,
                pet_create.name,
                pet_type.type
            )
            db.save_picture(filename, image_data)
            db.save_pet_url(pet_type.type, pet_create.name, pet_create.picture_url)
            
            # Update the pet with the new picture filename
            updated_pet = Pet(
                name=pet_create.name,
                birthdate=birthdate,
                picture=filename
            )
            db.update_pet(id, pet_create.name, updated_pet)
            pet = updated_pet  # Return the updated pet
            
        except HTTPException:
            print("HTTPException during picture download")
            db.delete_pet(id, pet_create.name)
            db.delete_picture(picture)
            db.delete_pet_url(pet_type.type, pet_create.name)
            raise
        except Exception:
            db.delete_pet(id, pet_create.name)
            db.delete_picture(picture)
            db.delete_pet_url(pet_type.type, pet_create.name)
            raise HTTPException(
                status_code=400,
                detail={"error": "Malformed data"}
            )

    # Return the created pet
    return pet

@router.get("", response_model=List[Pet])
def list_pets_for_type(
    id: str,
    birthdateGT: Optional[str] = None,
    birthdateLT: Optional[str] = None,
):
    """Get all pets of a pet type with optional filtering"""
    # Check if pet type exists
    pet_type = db.get_pet_type(id)
    if not pet_type:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    
    pets = db.get_all_pets(id)

    if birthdateGT or birthdateLT:
        filtered_pets = []

        gt_date = parse_date(birthdateGT) if birthdateGT else None
        lt_date = parse_date(birthdateLT) if birthdateLT else None

        for pet in pets:
            if pet.birthdate == "NA":
                continue
            
            pet_date = parse_date(pet.birthdate)
            if not pet_date:
                continue
            
            if gt_date and pet_date <= gt_date:
                continue
            
            if lt_date and pet_date >= lt_date:
                continue
            
            filtered_pets.append(pet)
        
        pets = filtered_pets
    
    return pets
        


@router.get("/{name}", response_model=Pet)
def get_pet(id: str, name: str):
    """Get a specific pet"""

    pet_type = db.get_pet_type(id)
    if not pet_type:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    
    pet = db.get_pet(id, name)
    if not pet:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    return pet


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(id: str, name: str):
    """Delete a pet"""
    # Check if pet type exists
    pet_type = db.get_pet_type(id)
    if not pet_type:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    

    # Check if pet exists
    pet = db.get_pet(id, name)
    if not pet:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    
    # Delete picture if exists
    if pet.picture != "NA":
        db.delete_picture(pet.picture)

    db.delete_pet(id, name)

    return

@router.put("/{name}", response_model=Pet)
def update_pet(id: str, name: str, pet_update: PetCreate):
    """Update a pet"""
    
    #Check if pet type exists
    pet_type = db.get_pet_type(id)
    if not pet_type:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    
    # Check if pet exists
    existing_pet = db.get_pet(id, name)
    if not existing_pet:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )
    
    birthdate = pet_update.birthdate if pet_update.birthdate else "NA"

    picture = existing_pet.picture
    if pet_update.picture_url:
        try:
            filename, image_data = ImageService.download_image(
                pet_update.picture_url,
                pet_update.name,
                pet_type.type
            )

            # Delete old picture if different
            if existing_pet.picture != "NA" and existing_pet.picture != filename:
                db.delete_picture(existing_pet.picture)
            
            db.save_picture(filename, image_data)
            picture = filename
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail={"error": "Malformed data"}
            )

    updated_pet = Pet(
            name=pet_update.name,
            birthdate=birthdate,
            picture=picture
        )
    
    db.update_pet(id, name, updated_pet)
    return updated_pet