from google import genai
from google.genai import types
import os

client = genai.Client()

model = genai.GenerativeModel('gemini-pro')

messages = []

while True:
    message = input("Awadhesh: ")
    messages.append({
        "role": "user",
        "parts": [message],
    })

    response = model.generate_content(messages)

    messages.append({
        "role": "model",
        "parts": [response.text],
    })

    print("Gemini: " + response.text)
 
