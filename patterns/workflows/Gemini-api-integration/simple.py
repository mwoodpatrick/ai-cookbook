# (quickstart)[https://ai.google.dev/gemini-api/docs/quickstart]
# (examples)[https://ai.google.dev/gemini-api/prompts]
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
    # (models)[https://ai.google.dev/gemini-api/docs/models]
    # (gemini-2.5-flash)[https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash]
    model='gemini-2.0-flash-001', 
    # model="gemini-2.5-flash",
    # model='gemini-2.5-pro', 
    contents='Why is the sky blue?',
    # Thinking is only available on Gemini 2.5 series models and can't be disabled on Gemini 2.5 Pro
    # only use for 2.5 models, czn't disable for pro
    # disable only enable for 
    # config=types.GenerateContentConfig(
    #    thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    # ),
)

print(response.text)
