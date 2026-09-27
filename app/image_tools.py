# Copyright 2026 Google LLC
# Image Generation Tools using gemini-3.1-flash-lite-image and Cloud Storage

import uuid
from typing import Dict, Any

from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

PROJECT_ID = "qwiklabs-gcp-03-e7a096ab7ace"
BUCKET_NAME = "real-estate-finder-media-qwiklabs-gcp-03-e7a096ab7ace"


async def generate_property_image(
    prompt: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """Generate a virtual room staging, property concept, or architectural image for a real estate listing.

    Args:
        prompt: Detailed description of the image to generate (e.g. 'Modern Scandinavian living room staging with large windows').
        tool_context: Injected ADK ToolContext used to save the generated image artifact.

    Returns:
        Dictionary containing prompt, public_url, and artifact_filename.
    """
    try:
        # Initialize Google GenAI client in global region
        genai_client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location="global",
        )
        
        # Generate image using gemini-3.1-flash-lite-image
        response = genai_client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=f"Generate a high-quality real estate photo: {prompt}",
        )
        
        image_bytes = None
        mime_type = "image/jpeg"
        
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    image_bytes = part.inline_data.data
                    if part.inline_data.mime_type:
                        mime_type = part.inline_data.mime_type
                    break
                    
        if not image_bytes:
            return {"error": f"Failed to generate image bytes for prompt: '{prompt}'."}
            
        unique_id = uuid.uuid4().hex[:8]
        filename = f"property_staging_{unique_id}.jpg"
        
        # 1. Save image as an artifact in Playground
        artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        await tool_context.save_artifact(filename=filename, artifact=artifact_part)
        
        # 2. Upload image bytes directly to GCS bucket (no local file write)
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type=mime_type)
        
        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
        
        return {
            "prompt": prompt,
            "public_url": public_url,
            "artifact_filename": filename,
            "message": "Image generated successfully, saved to Playground artifacts, and published to Cloud Storage.",
        }
    except Exception as e:
        return {"error": f"Failed to generate and store property image: {str(e)}"}
