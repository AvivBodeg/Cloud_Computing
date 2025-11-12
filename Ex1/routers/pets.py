from fastapi import APIRouter, HTTPException, status
from models.pet_type import PetType


router = APIRouter(prefix="/pet-types/{id}/pets", tags=["pets"])

#Create a new pet under the given pet-type.
@router.post("", response_model=Pet, status_code=status.HTTP_201_CREATED)
def create_pet(id: str, payload: dict):
    pass

#List all pets for the given pet-type.
@router.get("", response_model=List[Pet])
def list_pets_for_type(
    id: str,
    birthdateGT: Optional[str] = Query(None),
    birthdateLT: Optional[str] = Query(None),
):
    pass

#Get a specific pet by name under the given pet-type.
@router.get("/{name}", response_model=Pet)
def get_pet(id: str, name: str):
    pass

#DELETE /pet-types/{id}/pets/{name}
#Delete a specific pet by name under the given pet-type.
@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(id: str, name: str):
    pass


# PUT /pet-types/{id}/pets/{name}
# Update an existing pet under the given pet-type.
@router.put("/{name}", response_model=Pet)
def update_pet(id: str, name: str, payload: dict):
    pass































def list_pets_for_type(
    pet_type_id: str,
    birthdateGT: Optional[str] = Query(None),
    birthdateLT: Optional[str] = Query(None),
):

    # Parse a DD-MM-YYYY string to a date.
    def parser(date):
        if not date:
            return None
        try:
            return datetime.strptime(date.strip(), DATE_FMT).date()
        except ValueError:
            return None
        
    def get_id(s):
        if s not in db.pets_type:
            raise HTTPException(
            status_code=404,
            detail={"error": "Not found"}
        )

    def get_birthday(pet):
        if not p.birthday:
            return None
        try:
            return datetime.strptime(p.birthdate.strip(), DATE_FMT).date()
        except ValueError:
            return None
        
    def get_picture(p):
        return (p.picture or "").strip()
    
    ###main logic###

    get_id(pet_type_id)

    pets_dict = DB.pets_by_type.get(pet_type_id, {})
    pets = list(pets_dict.values())

    gt = parser(birthdateGT)
    lt = parser(birthdateLT)

    if not gt and not lt:
        return pets  # no filters

    filtered = []
    for p in pets:
        bd = get_birthday(p)
        if bd is None:
            # if there's a range filter, 'NA' birthdates never match
            continue
        if gt and not (bd > gt):
            continue
        if lt and not (bd < lt):
            continue
        # (optional) touch picture to normalize if you plan to use it later
        _ = get_picture(p)
        filtered.append(p)

    return filtered





    


    
    
