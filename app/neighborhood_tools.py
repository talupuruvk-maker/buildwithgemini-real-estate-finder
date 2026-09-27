# Copyright 2026 Google LLC
# Neighborhood & External API Tools for Real-Estate Agent

import os
import requests
from typing import Dict, Any


def lookup_zip_location(zip_code: str) -> Dict[str, Any]:
    """Lookup geographic and neighborhood location details for a US zip code using Zippopotam.us public API.

    Args:
        zip_code: 5-digit US postal zip code (e.g., '94122' or '95110').

    Returns:
        Dictionary containing city, state, state_abbreviation, latitude, and longitude.
    """
    cleaned_zip = zip_code.strip()[:5]
    url = f"http://api.zippopotam.us/us/{cleaned_zip}"
    
    headers = {}
    api_key = os.environ.get("ZIPPOPOTAMUS_API_KEY")
    if api_key:
        headers["X-Api-Key"] = api_key
        
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            places = data.get("places", [])
            if places:
                primary = places[0]
                return {
                    "zip_code": cleaned_zip,
                    "city": primary.get("place name"),
                    "state": primary.get("state"),
                    "state_abbreviation": primary.get("state abbreviation"),
                    "latitude": float(primary.get("latitude", 0)),
                    "longitude": float(primary.get("longitude", 0)),
                    "country": data.get("country"),
                }
        return {"error": f"No location data found for zip code '{zip_code}'."}
    except Exception as e:
        return {"error": f"Failed to fetch zip code location data: {str(e)}"}
