# https://googleapis.github.io/python-genai/
# https://pypi.org/project/google-genai/
#
# If you provide a list of strings then the SDK assumes these are 2 text parts, 
# it converts this into a single content, like the following:
#
#[
#   types.UserContent(
#    parts=[
#       types.Part.from_text(text='Why is the sky blue?'),
#       types.Part.from_text(text='Why is the cloud white?'),
#    ]
#   )
#]
from google import genai
from google.genai import types
import os

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=[
        'Why is the sky blue?',
        'Why is the cloud white?'
        ]
)

print(response.text)

