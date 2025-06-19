# https://googleapis.github.io/python-genai/
# https://pypi.org/project/google-genai/
from google import genai
from google.genai import types
import os

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue?'
)
print(response.text)
