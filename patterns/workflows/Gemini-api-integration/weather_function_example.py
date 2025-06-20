import google.generativeai as genai
import os
import json # For pretty printing tool calls
# --- 1. Configuration and API Key ---
# Make sure your GOOGLE_API_KEY environment variable is set
# export GOOGLE_API_KEY="YOUR_API_KEY" (Linux/macOS)
# set GOOGLE_API_KEY="YOUR_API_KEY" (Windows Cmd)
# $env:GOOGLE_API_KEY="YOUR_API_KEY" (Windows PowerShell)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# --- 2. Define Your Tools (Python Functions) ---
# Example: A function to get current weather data
def get_current_weather(location: str) -> dict:
    """Gets the current weather for a specified location.
Args:
        location: The city and state (e.g., "San Francisco, CA") or a zip code.
    """
    # In a real application, this would make an API call to a weather service.
    # For this example, we'll return simulated data.
    if "boston" in location.lower():
        return {
            "location": location,
            "temperature": "55F",
            "conditions": "Cloudy",
            "humidity": "80%"
        }
    elif "new york" in location.lower() or "nyc" in location.lower():
        return {
            "location": location,
            "temperature": "68F",
            "conditions": "Sunny",
            "humidity": "50%"
        }
    else:
        return {
            "location": location,
            "error": "Weather data not available for this location."
        }
# Example: A function to get current time for a city
def get_current_time(location: str) -> str:
    """Gets the current time for a specified location.
Args:
        location: The city (e.g., "London").
    """
    # In a real app, this would use a timezone API or similar.
    # Simulated data for example.
    if "london" in location.lower():
        return "10:30 AM GMT"
    elif "tokyo" in location.lower():
        return "6:30 PM JST"
    else:
        return f"Time for {location} is unknown."
# --- 3. Initialize the Model with Tools ---
# Pass your Python functions directly to the 'tools' parameter.
# The SDK automatically converts them into Function Declarations (schema).
model = genai.GenerativeModel(
    'gemini-1.5-flash', # Or 'gemini-1.5-pro' for more complex reasoning
    tools=[get_current_weather, get_current_time]
)
# Start a chat session. Using a ChatSession simplifies history management.
# automatic_function_calling=True is the default and makes the SDK
# automatically execute the function and send the result back to the model.
# If you set it to False, you'd manually handle part.function_call and part.function_response.
chat = model.start_chat(history=[])
# --- 4. User Interaction and Function Calling Flow ---
print("Chatbot: Hello! I can tell you the weather or current time for some cities.")
while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit"]:
        break
try:
        # Send the user message. If automatic_function_calling is True,
        # the SDK handles the execution of the tool and sends the result back to the model.
        # The final 'response' from model.send_message will be the text output.
        response = chat.send_message(user_message)
# Check if the model decided to call a function (even with auto-calling, you can inspect history)
        # This loop illustrates the steps if automatic_function_calling was False or for debugging
        for content in chat.history:
            for part in content.parts:
                if part.function_call:
                    print(f"\n[DEBUG] Model decided to call function: {part.function_call.name}")
                    print(f"[DEBUG] With arguments: {json.dumps(part.function_call.args, indent=2)}")
                    # If automatic_function_calling was False, you'd execute the function here
                    # and then send the FunctionResponse back to chat.send_message()
print(f"Chatbot: {response.text}")
except Exception as e:
        print(f"Chatbot: An error occurred: {e}")
        print("Chatbot: Please try again or rephrase your request.")
# --- 5. Inspecting Chat History (Optional) ---
# After the conversation, you can inspect the full history, including tool calls and responses.
# print("\n--- Full Chat History ---")
# for content in chat.history:
#     print(f"Role: {content.role}")
#     for part in content.parts:
#         if part.text:
#             print(f"  Text: {part.text}")
#         if part.function_call:
#             print(f"  Function Call: {part.function_call.name}({part.function_call.args})")
#         if part.function_response:
#             print(f"  Function Response: {part.function_response.name}: {part.function_response.response}")
#     print("-" * 20)

