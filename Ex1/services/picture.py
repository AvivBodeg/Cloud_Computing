import requests
from typing import Tuple, Optional
from fastapi import HTTPException

class ImageService:
    """Service for handling image downloads and storage"""
    
    @staticmethod
    def download_image(url: str, pet_name: str, pet_type: str, db=None) -> Tuple[str, Optional[bytes]]:
        """
        Download an image from URL
        Returns tuple of (filename, image_data)
        If image_data is None, it means we already have this file (URL was cached)
        """
        # Check if we already have this URL cached
        if db and hasattr(db, 'get_filename_for_url'):
            existing_filename = db.get_filename_for_url(url)
            if existing_filename and db.picture_exists(existing_filename):
                return existing_filename, None  # Return existing filename, no new data
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail={"error": "Malformed data"}
                )
            
            content_type = response.headers.get("Content-Type", "")
            
            if not content_type:
                raise HTTPException(
                    status_code=415,
                    detail={"error": "Unsupported Media Type"}
                )
            
            content_type = content_type.lower()
            
            if "jpeg" in content_type or "jpg" in content_type:
                extension = "jpg"
            elif "png" in content_type:
                extension = "png"
            else:
                raise HTTPException(
                    status_code=415,
                    detail={"error": "Unsupported Media Type"}
                )
            
            safe_pet_name = pet_name.replace(" ", "-").lower()
            safe_pet_type = pet_type.replace(" ", "-").lower()
            filename = f"{safe_pet_name}-{safe_pet_type}.{extension}"
            
            # Store URL mapping for future reference
            if db and hasattr(db, 'save_url_mapping'):
                db.save_url_mapping(url, filename)
            
            return filename, response.content
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=400,
                detail={"error": "Malformed data"}
            )
    
    @staticmethod
    def get_content_type(filename: str) -> str:
        """Get content type from filename"""
        if filename.lower().endswith(".png"):
            return "image/png"
        elif filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            return "image/jpeg"
        else:
            raise HTTPException(
                status_code=415,
                detail={"error": "Unsupported Media Type"}
            )