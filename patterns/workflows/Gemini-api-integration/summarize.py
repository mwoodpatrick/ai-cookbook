# https://googleapis.github.io/python-genai/
# https://pypi.org/project/google-genai/
from google import genai
from google.genai import types
import os

client = genai.Client()

file = client.files.upload(file='a11.txt')
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=['Could you summarize this file?', file]
)
print(response.text)
