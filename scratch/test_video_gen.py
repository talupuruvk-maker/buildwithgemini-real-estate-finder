import base64
import sys
import traceback
from google import genai

PROJECT_ID = "qwiklabs-gcp-03-e7a096ab7ace"

print("Starting script...", flush=True)

try:
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )
    print("GenAI client initialized with location=global.", flush=True)

    print("Calling client.interactions.create with gemini-omni-flash-preview...", flush=True)
    interaction = client.interactions.create(
        model="gemini-omni-flash-preview",
        input="A short 3-second property video tour of a modern open-concept living room."
    )
    print("SUCCESS: Interaction received!", flush=True)
    print("Interaction object:", interaction, flush=True)
except Exception as e:
    print("ERROR encountered:", str(e), flush=True)
    traceback.print_exc()
    sys.exit(1)
