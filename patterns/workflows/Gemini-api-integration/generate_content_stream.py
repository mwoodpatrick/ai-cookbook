# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model="gemini-2.0-flash-001"
    # model = "gemini-2.5-pro"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="Explain how AI works in a few words"),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        # thinking_config = types.ThinkingConfig(
        #    thinking_budget=-1,
        # ),
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()

