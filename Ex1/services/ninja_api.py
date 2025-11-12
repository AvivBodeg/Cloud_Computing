import os
import re
import requests
from typing import Optional, List
from fastapi import HTTPException

NINJA_API_KEY = "pSgkQKYWrLDlQI0Sg3zmLQ==RrHpVdqh8aCzByaQ"

class NinjaAPIService:
    BASE_URL = "https://api.api-ninjas.com/v1/animals"


    @staticmethod
    def get_animal_info(animal_type: str) -> dict:
        headers = {"X-Api-Key": NINJA_API_KEY}
        params = {"name": animal_type}
        try:
            response = requests.get(
                NinjaAPIService.BASE_URL,
                headers=headers,
                params=params
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail={"server_error": f"API response code {response.status_code}"}
                )
            
            data = response.json()

            if not data or len(data) == 0:
                raise HTTPException(
                    status_code=400,
                    detail={"error": "Malformed data"}
                )
            
            animal_type_lower = animal_type.lower()
            matched_animal = None

            for animal in data:
                if animal.get("name", "").lower() == animal_type_lower:
                    matched_animal = animal
                    break
            
            if not matched_animal:
                raise HTTPException(
                    status_code=400,
                    detail={"error": "Malformed data"}
                )
            
            family = matched_animal.get("taxonomy", {}).get("family", "")
            genus = matched_animal.get("taxonomy", {}).get("genus", "")

            attributes = []
            if "characteristics" in matched_animal:
                chars = matched_animal["characteristics"]
                if "temperament" in chars and chars["temperament"]:
                    attributes = NinjaAPIService._extract_attributes(chars["temperament"])
                elif "group_behavior" in chars and chars["group_behavior"]:
                    attributes = NinjaAPIService._extract_attributes(chars["group_behavior"])
            
            lifespan = None
            if "characteristics" in matched_animal and "lifespan" in matched_animal["characteristics"]:
                lifespan_str = matched_animal["characteristics"]["lifespan"]
                lifespan = NinjaAPIService._parse_lifespan(lifespan_str)
            
            return {
                "family": family,
                "genus": genus,
                "attributes": attributes,
                "lifespan": lifespan
            }
        
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail={"server_error": f"Request failed: {str(e)}"}
            )

        

    @staticmethod
    def _extract_attributes(entry: str) -> List[str]:
        if not entry:
            return []

        text = re.sub(r'[^\w\s]', ' ', entry)
        return [word for word in text.split() if word]


    @staticmethod
    def _parse_lifespan(lifespan_str: str) -> Optional[float]:
        if not lifespan_str:
            return None
        
        numbers = re.findall(r'(\d+)', lifespan_str)
        if numbers:
            return int(min( numbers, key=int))
        
        return None