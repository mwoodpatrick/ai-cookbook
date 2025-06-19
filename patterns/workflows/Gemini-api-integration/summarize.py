# https://googleapis.github.io/python-genai/
# https://pypi.org/project/google-genai/
from google import genai
from google.genai import types
import os

client = genai.Client()

# wget -q https://storage.googleapis.com/generativeai-downloads/data/a11.txt
file = client.files.upload(file='a11.txt')

# How to structure contents argument for generate_content
# The SDK always converts the inputs to the contents argument into list[types.Content]. 
# Use a file
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=['Could you summarize this file?', file]
)
print(response.text)
