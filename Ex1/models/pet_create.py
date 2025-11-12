from pydantic import BaseModel
from typing import Optional

class PetTypeCreate(BaseModel):
    name: str
    birthday: Optional[str]
    picture: Optional[str]