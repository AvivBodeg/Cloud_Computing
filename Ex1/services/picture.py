import requests
from typing import Tuple
from fastapi import HTTPException

class ImageService:
    """Service for handling image downloads and storage"""
    
    @staticmethod
    def download_image(url: str, pet_name: str, pet_type: str) -> Tuple[str, bytes]:
        """
        Download an image from URL
        Returns tuple of (filename, image_data)
        """
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail={"error": "Malformed data"}
                )
            
            content_type = response.headers.get("Content-Type", "")
            print(f"Content-Type received from URL: '{content_type}'")
            
            if not content_type:
                print("No Content-Type header found in response")
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
                # Debug: Print the actual content type received
                print(f"Unsupported Content-Type received: '{content_type}'")
                raise HTTPException(
                    status_code=415,
                    detail={"error": "Unsupported Media Type"}
                )
            
            safe_pet_name = pet_name.replace(" ", "-").lower()
            safe_pet_type = pet_type.replace(" ", "-").lower()
            filename = f"{safe_pet_name}-{safe_pet_type}.{extension}"
            
            return filename, response.content
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=400,
                detail={"error": "Malformed data"}
            )
    
    @staticmethod
    def get_content_type(filename: str) -> str:
        """Get content type from filename"""
        filename_lower = filename.lower()
        if filename_lower.endswith(".png"):
            return "image/png"
        elif filename_lower.endswith(".jpg") or filename_lower.endswith(".jpeg"):
            return "image/jpeg"
        else:
            print(f"Unsupported filename extension: '{filename}'")
            raise HTTPException(
                status_code=415,
                detail={"error": "Unsupported Media Type"}
            )