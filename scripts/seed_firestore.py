# Copyright 2026 Google LLC
# Seed script for Real-Estate & Neighborhood Finder Firestore Database

import os
from google.cloud import firestore

# Hardcode project ID explicitly as required (do NOT use google.auth.default() or GOOGLE_CLOUD_PROJECT)
PROJECT_ID = "qwiklabs-gcp-03-e7a096ab7ace"
COLLECTION_NAME = "properties"

SAMPLE_PROPERTIES = [
    {
        "id": "prop-101",
        "title": "Modern Sunset Heights Condo",
        "address": "1240 19th Ave",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94122",
        "price": 850000,
        "beds": 2,
        "baths": 2.0,
        "sqft": 1100,
        "property_type": "Condo",
        "description": "Bright and airy modern condo in Inner Sunset with private balcony, ocean views, and upgraded kitchen.",
        "walk_score": 88,
        "school_rating": 9,
        "hoa_fee": 350,
        "image_url": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80",
    },
    {
        "id": "prop-102",
        "title": "Pacific Heights Victorian Residence",
        "address": "2104 Broadway St",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94115",
        "price": 2450000,
        "beds": 4,
        "baths": 3.5,
        "sqft": 2800,
        "property_type": "Single Family",
        "description": "Stunning renovated Victorian with original molding, high ceilings, gourmet kitchen, and private garden yard.",
        "walk_score": 95,
        "school_rating": 10,
        "hoa_fee": 0,
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
    },
    {
        "id": "prop-103",
        "title": "Mission District Industrial Loft",
        "address": "680 Valencia St",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94110",
        "price": 695000,
        "beds": 1,
        "baths": 1.5,
        "sqft": 950,
        "property_type": "Condo",
        "description": "Spacious open-concept industrial loft with concrete floors, floor-to-ceiling windows, and rooftop deck access.",
        "walk_score": 98,
        "school_rating": 7,
        "hoa_fee": 420,
        "image_url": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80",
    },
    {
        "id": "prop-104",
        "title": "Bayview Modern Townhouse",
        "address": "1450 Egbert Ave",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94124",
        "price": 980000,
        "beds": 3,
        "baths": 2.5,
        "sqft": 1650,
        "property_type": "Townhouse",
        "description": "Contemporary 3-story townhouse with attached 2-car garage, solar panels, and low HOA fees.",
        "walk_score": 75,
        "school_rating": 8,
        "hoa_fee": 210,
        "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
    },
    {
        "id": "prop-105",
        "title": "Silicon Valley Family Residence",
        "address": "382 Willow St",
        "city": "San Jose",
        "state": "CA",
        "zip_code": "95110",
        "price": 1350000,
        "beds": 4,
        "baths": 3.0,
        "sqft": 2200,
        "property_type": "Single Family",
        "description": "Charming family home in quiet neighborhood close to tech campuses, top-rated schools, and parks.",
        "walk_score": 82,
        "school_rating": 9,
        "hoa_fee": 0,
        "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=800&q=80",
    },
]


def seed_firestore():
    print(f"Connecting to Firestore for project '{PROJECT_ID}'...")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    print(f"Seeding '{COLLECTION_NAME}' collection...")
    for prop in SAMPLE_PROPERTIES:
        doc_ref = collection_ref.document(prop["id"])
        doc_ref.set(prop)
        print(f"  ✓ Added property {prop['id']}: {prop['title']} (${prop['price']:,})")

    print("Successfully seeded Firestore properties collection!")


if __name__ == "__main__":
    seed_firestore()
