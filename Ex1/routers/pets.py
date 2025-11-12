from fastapi import APIRouter, HTTPException, status
from models.pet_type import PetType
from models.pet_create import PetCreate
from models.pet import Pet
from database.memory_db import db


router = APIRouter(prefix="/pet-types/{id}/pets", tags=["pets"])

#Create a new pet under the given pet-type.
@router.post("", response_model=Pet, status_code=status.HTTP_201_CREATED)
def create_pet(id: str, pet_create: PetCreate):
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
    picture = pet_create.picture or "NA"
    #TODO: get and verify picture

    try:
        pet = Pet(
            name=pet_create.name,
            birthdate=birthdate,
            picture=picture
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "Malformed data"}
        )

    # Add the pet to the database
    success = db.add_pet(id, pet)
    if not success:
        raise HTTPException(
            status_code=500,
            detail={"server_error": "Failed to add pet"} # TODO: change error code
        )

    # Return the created pet
    return pet

# #List all pets for the given pet-type.
# @router.get("", response_model=List[Pet])
# def list_pets_for_type(
#     id: str,
#     birthdateGT: Optional[str] = Query(None),
#     birthdateLT: Optional[str] = Query(None),
# ):
#     pet_type = db.get("pet_types", {}).get(id)
#     if not pet_type:
#         raise HTTPException(404, "pet-type not found")
    
#     pets_dict = getattr(pet_type, "pets", None) or db.get("pets_by_type", {}).get(id, {})
#     pets_list = list(pets_dict.values())

#     gt = None
#     lt = None
#     if birthdateGT is not None:
#         try:
#             gt = date.fromisoformat(birthdateGT)
#         except ValueError:
#             raise HTTPException(400, "invalid birthdateGT: expected YYYY-MM-DD")
#     if birthdateLT is not None:
#         try:
#             lt = date.fromisoformat(birthdateLT)
#         except ValueError:
#             raise HTTPException(400, "invalid birthdateLT: expected YYYY-MM-DD")

#     if gt or lt:
#         out = []
#         for p in pets_list:
#             bd = p.birthdate if isinstance(p.birthdate, date) else date.fromisoformat(str(p.birthdate))
#             if gt and not (bd > gt):
#                 continue
#             if lt and not (bd < lt):
#                 continue
#             out.append(p)
#         return out

#     return pets_list


# #Get a specific pet by name under the given pet-type.
# @router.get("/{name}", response_model=Pet)
# def get_pet(id: str, name: str):
#     pet_type = db.get("pet_types", {}).get(id)
#     if not pet_type:
#         raise HTTPException(404, "pet-type not found")
    
#     pets_dict = getattr(pet_type, "pets", None) or db.get("pets_by_type", {}).get(id, {})
#     pet = pets_dict.get(name)
#     if not pet:
#         raise HTTPException(404, "pet not found")
#     return pet


# #DELETE /pet-types/{id}/pets/{name}
# #Delete a specific pet by name under the given pet-type.
# @router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_pet(id: str, name: str):
#     pet_type = db.get("pet_types", {}).get(id)
#     if not pet_type:
#         raise HTTPException(404, "pet-type not found")

#     pets_dict = getattr(pet_type, "pets", None) or db.get("pets_by_type", {}).get(id, {})
#     if name not in pets_dict:
#         raise HTTPException(404, "pet not found")

#     del pets_dict[name]
#     if hasattr(pet_type, "pets"):
#         pet_type.pets = pets_dict
#     return



# # PUT /pet-types/{id}/pets/{name}
# # Update an existing pet under the given pet-type.
# @router.put("/{name}", response_model=Pet)
# def update_pet(id: str, name: str, payload: dict):
#     pet_type = db.get("pet_types", {}).get(id)
#     if not pet_type:
#         raise HTTPException(404, "pet-type not found")

#     pets_dict = getattr(pet_type, "pets", None) or db.get("pets_by_type", {}).get(id, {})
#     if name not in pets_dict:
#         raise HTTPException(404, "pet not found")

#     try:
#         pet = Pet(**payload)
#     except Exception as e:
#         raise HTTPException(400, f"invalid pet payload: {e}")

    
#     if pet.name != name:
#         raise HTTPException(409, "pet name in payload must match the path parameter")

#     pets_dict[name] = pet
#     if hasattr(pet_type, "pets"):
#         pet_type.pets = pets_dict
#     return pet
