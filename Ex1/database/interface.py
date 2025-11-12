from abc import ABC, abstractmethod
from typing import List, Optional
from models.pet_type import PetType
from models.pet import Pet

class DatabaseInterface(ABC):
    """Abstract interface for database operations"""
    
    @abstractmethod
    def add_pet_type(self, pet_type: PetType) -> bool:
        """Add a new pet type to the database"""
        pass
    
    @abstractmethod
    def get_pet_type(self, pet_type_id: str) -> Optional[PetType]:
        """Get a pet type by ID"""
        pass
    
    @abstractmethod
    def get_all_pet_types(self) -> List[PetType]:
        """Get all pet types"""
        pass
    
    @abstractmethod
    def delete_pet_type(self, pet_type_id: str) -> bool:
        """Delete a pet type by ID. Returns True if successful."""
        pass
    
    @abstractmethod
    def pet_type_exists(self, type_name: str) -> bool:
        """Check if a pet type with the given name exists"""
        pass
    
    @abstractmethod
    def add_pet(self, pet_type_id: str, pet: Pet) -> bool:
        """Add a pet to a pet type"""
        pass
    
    @abstractmethod
    def get_pet(self, pet_type_id: str, pet_name: str) -> Optional[Pet]:
        """Get a pet by pet type ID and name"""
        pass
    
    @abstractmethod
    def get_all_pets(self, pet_type_id: str) -> List[Pet]:
        """Get all pets of a specific pet type"""
        pass
    
    @abstractmethod
    def update_pet(self, pet_type_id: str, pet_name: str, pet: Pet) -> bool:
        """Update a pet. Returns True if successful."""
        pass
    
    @abstractmethod
    def delete_pet(self, pet_type_id: str, pet_name: str) -> bool:
        """Delete a pet. Returns True if successful."""
        pass
    
    @abstractmethod
    def pet_exists(self, pet_type_id: str, pet_name: str) -> bool:
        """Check if a pet exists"""
        pass
    
    @abstractmethod
    def save_picture(self, file_name: str, image_data: bytes) -> None:
        """Save a picture file"""
        pass
    
    @abstractmethod
    def get_picture(self, file_name: str) -> Optional[bytes]:
        """Get a picture file"""
        pass
    
    @abstractmethod
    def delete_picture(self, file_name: str) -> bool:
        """Delete a picture file. Returns True if successful."""
        pass
    
    @abstractmethod
    def picture_exists(self, file_name: str) -> bool:
        """Check if a picture exists"""
        pass