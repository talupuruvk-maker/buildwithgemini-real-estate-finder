import asyncio
import sys
import traceback
from google.adk.tools import ToolContext
from app.video_tools import generate_property_video

class MockToolContext(ToolContext):
    def __init__(self):
        self.saved_artifacts = []
    
    async def save_artifact(self, filename: str, artifact: any) -> None:
        mime = getattr(artifact.inline_data, "mime_type", "unknown") if hasattr(artifact, "inline_data") else "unknown"
        data_len = len(artifact.inline_data.data) if hasattr(artifact, "inline_data") and artifact.inline_data else 0
        print(f"MockToolContext: Saved artifact '{filename}' (mime_type={mime}, bytes={data_len})", flush=True)
        self.saved_artifacts.append((filename, artifact))

async def test_tool():
    ctx = MockToolContext()
    prompt = "A 3-second virtual walkthrough video of a modern kitchen with island."
    print("Testing generate_property_video tool...", flush=True)
    res = await generate_property_video(prompt=prompt, tool_context=ctx)
    print("\nTool result:", res, flush=True)
    assert "public_url" in res, f"public_url missing from tool output: {res}"
    assert "artifact_filename" in res, "artifact_filename missing from tool output"
    assert res["public_url"].startswith("https://storage.googleapis.com/real-estate-finder-media-qwiklabs-gcp-03-e7a096ab7ace/"), f"Unexpected URL: {res.get('public_url')}"
    print("\nTEST PASSED SUCCESSFULLY!", flush=True)

if __name__ == "__main__":
    asyncio.run(test_tool())
