# Copyright 2026 Google LLC
# Firestore tools for Real-Estate & Neighborhood Finder Agent

import uuid
from typing import Optional, List, Dict, Any
from google.cloud import firestore

# Hardcode project ID explicitly as required (do NOT read from google.auth.default() or GOOGLE_CLOUD_PROJECT)
PROJECT_ID = "qwiklabs-gcp-03-e7a096ab7ace"
COLLECTION_NAME = "properties"


def _get_db() -> firestore.Client:
    """Returns a Firestore client initialized with the hardcoded project ID."""
    return firestore.Client(project=PROJECT_ID)


def search_properties(
    city: Optional[str] = None,
    max_price: Optional[float] = None,
    min_beds: Optional[int] = None,
    property_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search for real estate property listings in Firestore based on criteria.

    Args:
        city: Optional city name to filter listings (e.g., 'San Francisco', 'San Jose').
        max_price: Optional maximum price limit in USD.
        min_beds: Optional minimum number of bedrooms.
        property_type: Optional type of property (e.g., 'Condo', 'Single Family', 'Townhouse').

    Returns:
        List of property listing dictionaries matching the specified criteria.
    """
    db = _get_db()
    docs = db.collection(COLLECTION_NAME).stream()
    
    results = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        
        if city and city.lower() not in data.get("city", "").lower():
            continue
        if max_price is not None and data.get("price", 0) > float(max_price):
            continue
        if min_beds is not None and data.get("beds", 0) < int(min_beds):
            continue
        if property_type and property_type.lower() not in data.get("property_type", "").lower():
            continue
            
        results.append(data)
        
    return results


def get_property_details(property_id: str) -> Dict[str, Any]:
    """Retrieve complete details for a specific real estate property by its document ID.

    Args:
        property_id: The unique document ID of the property (e.g., 'prop-101').

    Returns:
        Dictionary containing property details, or an error dictionary if not found.
    """
    db = _get_db()
    doc_ref = db.collection(COLLECTION_NAME).document(property_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return {"error": f"Property with ID '{property_id}' not found."}
        
    data = doc.to_dict()
    data["id"] = doc.id
    return data


def add_property(
    title: str,
    address: str,
    city: str,
    zip_code: str,
    price: float,
    beds: int,
    baths: float,
    sqft: int,
    property_type: str,
    description: str,
    state: str = "CA",
    walk_score: int = 80,
    school_rating: int = 8,
    hoa_fee: int = 0,
    image_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Add a new property listing to the Firestore database.

    Args:
        title: Title/name of the listing (e.g., 'Modern Sunset Heights Condo').
        address: Street address of the property.
        city: City where the property is located.
        zip_code: Postal code of the property.
        price: Price of the property in USD.
        beds: Number of bedrooms.
        baths: Number of bathrooms.
        sqft: Square footage of the property.
        property_type: Type of property ('Condo', 'Single Family', 'Townhouse').
        description: Detailed summary or feature description.
        state: Two-letter state code (default 'CA').
        walk_score: Walkability score from 0-100 (default 80).
        school_rating: Nearby school rating from 1-10 (default 8).
        hoa_fee: Monthly HOA fee in USD (default 0).
        image_url: Optional image URL for the property.

    Returns:
        Dictionary containing the saved property details including the newly generated property ID.
    """
    db = _get_db()
    prop_id = f"prop-{uuid.uuid4().hex[:6]}"
    
    property_data = {
        "id": prop_id,
        "title": title,
        "address": address,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "price": float(price),
        "beds": int(beds),
        "baths": float(baths),
        "sqft": int(sqft),
        "property_type": property_type,
        "description": description,
        "walk_score": int(walk_score),
        "school_rating": int(school_rating),
        "hoa_fee": int(hoa_fee),
        "image_url": image_url or "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80",
    }
    
    db.collection(COLLECTION_NAME).document(prop_id).set(property_data)
    return property_data
