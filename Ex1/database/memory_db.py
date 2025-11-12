from .interface import DatabaseInterface
from typing import Dict, List, Optional
from models.pet_type import PetType
from models.pet import Pet

class InMemoryDatabase(DatabaseInterface):
    def __init__(self):
        self.pet_types: Dict[str, PetType] = {}
        self.pets: Dict[str, Dict[str, Pet]] = {}
        self.pictures: Dict[str, bytes] = {}
        self.next_id = 1
        self.used_ids = set()
    
    def generate_id(self) -> str:
            while str(self.next_id) in self.used_ids:
                self.next_id += 1
            id_str = str(self.next_id)
            self.used_ids.add(id_str)
            self.next_id += 1
            return id_str

    def add_pet_type(self, pet_type: PetType) -> bool:
        self.pet_types[pet_type.id] = pet_type
        if pet_type.id not in self.pets:
            self.pets[pet_type.id] = {}
            return True
        return False
    
    def get_pet_type(self, pet_type_id: str) -> Optional[PetType]:
        return self.pet_types.get(pet_type_id)
    
    def get_all_pet_types(self) -> List[PetType]:
        return list(self.pet_types.values())
    
    def delete_pet_type(self, pet_type_id: str) -> bool:
        if pet_type_id in self.pet_types:
            del self.pet_types[pet_type_id]
            if pet_type_id in self.pets:
                del self.pets[pet_type_id]
            return True
        return False
    
    def pet_type_exists(self, type_name: str) -> bool:
        type_name_lower = type_name.lower()
        return any(pt.type.lower() == type_name_lower for pt in self.pet_types.values())
    
    def add_pet(self, pet_type_id: str, pet: Pet) -> bool:
        if pet_type_id not in self.pets:
            return False

        if not any(existing_name.lower() == pet.name.lower() for existing_name in self.pets[pet_type_id].keys()):
            self.pet_types[pet_type_id].pets.append(pet.name)
            self.pets[pet_type_id][pet.name] = pet
            return True
        return False

    def get_pet(self, pet_type_id: str, pet_name: str) -> Optional[Pet]:
        if pet_type_id in self.pets:
            for stored_name, pet in self.pets[pet_type_id].items():
                if stored_name.lower() == pet_name.lower():
                    return pet
        return None
    
    def get_all_pets(self, pet_type_id: str) -> List[Pet]:
        if pet_type_id in self.pets:
            return list(self.pets[pet_type_id].values())
        return []
    
    def update_pet(self, pet_type_id: str, pet_name: str, pet: Pet) -> bool:
        if pet_type_id in self.pets:
            # Find the pet with case-insensitive comparison
            stored_name = None
            for name in self.pets[pet_type_id].keys():
                if name.lower() == pet_name.lower():
                    stored_name = name
                    break
            
            if stored_name:
                old_pet = self.pets[pet_type_id][stored_name]
                # Remove old entry
                del self.pets[pet_type_id][stored_name]
                # Add with new name (exact case)
                self.pets[pet_type_id][pet.name] = pet
                
                # Update the pet_type's pets list
                if pet_type_id in self.pet_types:
                    pets_list = self.pet_types[pet_type_id].pets
                    if old_pet.name in pets_list:
                        pets_list.remove(old_pet.name)
                    pets_list.append(pet.name)
                
                return True
        return False
    
    def delete_pet(self, pet_type_id: str, pet_name: str) -> bool:
        if pet_type_id in self.pets:
            # Find the pet with case-insensitive comparison
            stored_name = None
            for name in self.pets[pet_type_id].keys():
                if name.lower() == pet_name.lower():
                    stored_name = name
                    break
            
            if stored_name:
                pet = self.pets[pet_type_id][stored_name]
                del self.pets[pet_type_id][stored_name]
                
                # Update the pet_type's pets list
                if pet_type_id in self.pet_types:
                    if pet.name in self.pet_types[pet_type_id].pets:
                        self.pet_types[pet_type_id].pets.remove(pet.name)
                
                return True
        return False
    
    def pet_exists(self, pet_type_id: str, pet_name: str) -> bool:
        if pet_type_id in self.pets:
            # Check existence with case-insensitive comparison
            return any(stored_name.lower() == pet_name.lower() for stored_name in self.pets[pet_type_id].keys())
        return False
    
    def save_picture(self, file_name: str, image_data: bytes) -> None:
        self.pictures[file_name] = image_data
    
    def get_picture(self, file_name: str) -> Optional[bytes]:
        return self.pictures.get(file_name)
    
    def delete_picture(self, file_name: str) -> bool:
        if file_name in self.pictures:
            del self.pictures[file_name]
            return True
        return False
    
    def picture_exists(self, file_name: str) -> bool:
        return file_name in self.pictures

# Global database instance
db = InMemoryDatabase()