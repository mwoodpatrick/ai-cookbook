# see python-genai/google/genai/tests/models/test_list.py
from google import genai
from google.genai import types
import os

client = genai.Client()

print("Checking for available models with the provided API key...")

try:
    for model in client.models.list():
        # Models can support different generation methods.
        # 'generateContent' is a common method for text and multimodal generation.
        # 'embedContent' is for creating text embeddings.
        if 'generateContent' in model.supported_actions:
            print(f"{model.name} - {model.display_name} - {model.description}")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure your API key is valid and has the necessary permissions.")
