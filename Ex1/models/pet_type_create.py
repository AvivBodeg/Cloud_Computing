from pydantic import BaseModel

class PetTypeCreate(BaseModel):
    type: str