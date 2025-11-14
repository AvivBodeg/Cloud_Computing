from pydantic import BaseModel
from typing import Optional

class PetCreate(BaseModel):
    name: str
    birthdate: Optional[str] = None
    picture_url: Optional[str] = None