# https://googleapis.github.io/python-genai/
# https://pypi.org/project/google-genai/
#
# The SDK always converts the inputs to the contents argument into list[types.Content]. 
# The following shows some common ways to provide your inputs.
# So the above contents example where a string is provided the SDK converts it into:
# [
#   types.UserContent(
#       parts=[
#           types.Part.from_text(text='Why is the sky blue?')
#       ]
#   )
# ]
#
# Where a types.UserContent is a subclass of types.Content, it sets the role field to be user.

from google import genai
from google.genai import types
import os

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    # model='gemini-2.5-pro', 
    contents='Why is the sky blue?'
)

print(response.text)
