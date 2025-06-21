from google import genai
from google.genai import types
import os

# It's recommended to set your API key as an environment variable
# for security purposes.
try:
    # Or, you can directly pass your key to genai.configure(api_key="YOUR_API_KEY")
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Please set the GOOGLE_API_KEY environment variable.")
    exit()

print("Checking for available models with the provided API key...")

try:
    for model in genai.list_models():
        # Models can support different generation methods.
        # 'generateContent' is a common method for text and multimodal generation.
        # 'embedContent' is for creating text embeddings.
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure your API key is valid and has the necessary permissions.")
