# Copyright 2026 Google LLC
# Video Generation Tool using gemini-omni-flash-preview and Cloud Storage

import base64
import uuid
from typing import Dict, Any

from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

PROJECT_ID = "qwiklabs-gcp-03-e7a096ab7ace"
BUCKET_NAME = "real-estate-finder-media-qwiklabs-gcp-03-e7a096ab7ace"


async def generate_property_video(
    prompt: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """Generate a short virtual walkthrough or showcase video for a real estate listing or neighborhood.

    Args:
        prompt: Detailed description of the video to generate (e.g. '3-second smooth virtual tour of a modern open-concept living room with large windows').
        tool_context: Injected ADK ToolContext used to save the generated video artifact.

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
        
        # Generate video using gemini-omni-flash-preview via Interactions API
        interaction = genai_client.interactions.create(
            model="gemini-omni-flash-preview",
            input=f"Generate a short high-quality real estate video tour: {prompt}",
        )
        
        video_bytes = None
        mime_type = "video/mp4"
        
        if hasattr(interaction, "output_video") and interaction.output_video and getattr(interaction.output_video, "data", None):
            raw_data = interaction.output_video.data
            if isinstance(raw_data, str):
                video_bytes = base64.b64decode(raw_data)
            else:
                video_bytes = raw_data
        elif hasattr(interaction, "outputs") and interaction.outputs:
            for out in interaction.outputs:
                if getattr(out, "type", "") == "video" or getattr(out, "mime_type", "").startswith("video/"):
                    raw_data = getattr(out, "data", None)
                    if raw_data:
                        if isinstance(raw_data, str):
                            video_bytes = base64.b64decode(raw_data)
                        else:
                            video_bytes = raw_data
                        break
                    
        if not video_bytes:
            return {"error": f"Failed to extract video bytes for prompt: '{prompt}'."}
            
        unique_id = uuid.uuid4().hex[:8]
        filename = f"property_tour_{unique_id}.mp4"
        
        # 1. Save video as an artifact in Playground
        artifact_part = types.Part.from_bytes(data=video_bytes, mime_type=mime_type)
        await tool_context.save_artifact(filename=filename, artifact=artifact_part)
        
        # 2. Upload video bytes directly to public GCS bucket (no local file write)
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(video_bytes, content_type=mime_type)
        
        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
        
        return {
            "prompt": prompt,
            "public_url": public_url,
            "artifact_filename": filename,
            "message": "Video generated successfully, saved to Playground artifacts, and published to Cloud Storage.",
        }
    except Exception as e:
        return {"error": f"Failed to generate and store property video: {str(e)}"}
