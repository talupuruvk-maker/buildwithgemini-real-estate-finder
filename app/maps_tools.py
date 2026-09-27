# Copyright 2026 Google LLC
# Google Maps Geocoding and Places (New) API tools for Real-Estate Agent

import os
import requests
from typing import Dict, Any, List, Optional

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _get_maps_api_key() -> str:
    """Retrieve Google Maps API key from environment variable."""
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set. Please add it to your .env file.")
    return api_key.strip()


def geocode_address(address: str) -> Dict[str, Any]:
    """Turn a street address or location name into geographic coordinates (latitude and longitude).

    Args:
        address: Full street address or landmark (e.g., '1240 19th Ave, San Francisco, CA').

    Returns:
        Dictionary with formatted_address, location (latitude, longitude), and place_id.
    """
    api_key = _get_maps_api_key()
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key,
    }
    
    try:
        response = requests.get(url, params=params, timeout=8)
        data = response.json()
        
        if data.get("status") == "OK" and data.get("results"):
            result = data["results"][0]
            loc = result.get("geometry", {}).get("location", {})
            return {
                "address": address,
                "formatted_address": result.get("formatted_address"),
                "location": {
                    "latitude": loc.get("lat"),
                    "longitude": loc.get("lng"),
                },
                "place_id": result.get("place_id"),
            }
        return {"error": f"Geocoding failed for address '{address}'. Status: {data.get('status')}"}
    except Exception as e:
        return {"error": f"Geocoding API request failed: {str(e)}"}


def find_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "school",
    radius_meters: float = 1000.0,
    max_results: int = 5,
) -> List[Dict[str, Any]]:
    """Find nearby places of a given type around latitude and longitude using Google Places API (New).

    Args:
        latitude: Latitude coordinate of the central location.
        longitude: Longitude coordinate of the central location.
        place_type: Type of place to search for (e.g., 'school', 'park', 'restaurant', 'cafe', 'transit_station').
        radius_meters: Search radius in meters (default 1000.0 meters).
        max_results: Maximum number of place results to return (default 5).

    Returns:
        List of dictionaries with name, address, and location (latitude, longitude).
    """
    api_key = _get_maps_api_key()
    url = "https://places.googleapis.com/v1/places:searchNearby"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.types",
    }
    
    # Map friendly type names to Places API (New) Table A/B types if needed
    type_clean = place_type.lower().strip()
    
    payload = {
        "includedTypes": [type_clean],
        "maxResultCount": int(max_results),
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": float(latitude),
                    "longitude": float(longitude),
                },
                "radius": float(radius_meters),
            }
        },
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        data = response.json()
        
        places_list = data.get("places", [])
        results = []
        for p in places_list:
            display_name = p.get("displayName", {}).get("text", "Unknown Place")
            loc = p.get("location", {})
            results.append({
                "name": display_name,
                "address": p.get("formattedAddress"),
                "location": {
                    "latitude": loc.get("latitude"),
                    "longitude": loc.get("longitude"),
                },
            })
            
        return results
    except Exception as e:
        return [{"error": f"Places API (New) search failed: {str(e)}"}]
