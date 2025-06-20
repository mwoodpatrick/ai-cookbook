from google import genai
from google.genai import types
import os
import json # For pretty printing tool calls for demonstration

# --- 1. Configuration: Set your API key ---
# It's highly recommended to store your API key as an environment variable
# named GOOGLE_API_KEY. The SDK will automatically pick it up.
#
# On Linux/macOS: export GOOGLE_API_KEY="YOUR_API_KEY"
# On Windows Cmd: set GOOGLE_API_KEY="YOUR_API_KEY"
# On Windows PowerShell: $env:GOOGLE_API_KEY="YOUR_API_KEY"
#
# Alternatively, you can configure it directly in code (less secure for production):
# genai.configure(api_key="YOUR_API_KEY")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- 2. Define Your Tool (Python Function) ---
# The SDK uses the function signature (name, arguments, type hints)
# and its docstring to automatically create the FunctionDeclaration schema.

def get_current_weather(location: str, unit: str = "fahrenheit") -> dict:
    """Gets the current weather for a specified location.

    Args:
        location: The city and state (e.g., "Boston, MA" or "London, UK").
        unit: The unit of temperature. Can be "celsius" or "fahrenheit". Defaults to "fahrenheit".
    """
    # --- This is where your actual API call to a weather service would go ---
    # For this example, we'll return simulated data based on the location.
    location_lower = location.lower()
    if "boston" in location_lower:
        temp_f = 55
        temp_c = 13
        conditions = "Cloudy"
        humidity = "80%"
    elif "new york" in location_lower or "nyc" in location_lower:
        temp_f = 68
        temp_c = 20
        conditions = "Sunny"
        humidity = "50%"
    elif "london" in location_lower:
        temp_f = 60
        temp_c = 16
        conditions = "Partly Cloudy"
        humidity = "70%"
    else:
        return {"location": location, "error": "Weather data not available for this location."}

    temperature = temp_c if unit.lower() == "celsius" else temp_f
    unit_symbol = "°C" if unit.lower() == "celsius" else "°F"

    return {
        "location": location,
        "temperature": f"{temperature}{unit_symbol}",
        "conditions": conditions,
        "humidity": humidity
    }

# --- 3. Initialize the Model with Tools ---
# Pass your Python functions in a list to the 'tools' parameter.
# The SDK automatically generates the necessary Function Declarations (schemas) for the model.
model = genai.GenerativeModel(
    'gemini-1.5-flash', # Use a Gemini model that supports function calling
    tools=[get_current_weather]
)

# Start a chat session. The 'enable_automatic_function_calling=True' (which is default)
# simplifies the process by making the SDK automatically execute the function call
# and feed its result back to the model before returning the text response.
chat = model.start_chat(history=[])

# --- 4. User Interaction and Function Calling Flow ---

print("Chatbot: Hello! I can tell you the current weather for some major cities like Boston, New York, or London.")
print("Chatbot: You can also specify Celsius or Fahrenheit.")

while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit"]:
        break

    try:
        # Send the user's message.
        # If the model decides to call a tool, the SDK (because automatic_function_calling=True)
        # will execute the function and then send the result back to the model in an
        # internal turn before returning the final text response.
        response = chat.send_message(user_message)

        # --- Debugging/Observing the Function Call (Optional) ---
        # This part helps you see what happened behind the scenes.
        # You'd typically only use this for debugging or if automatic_function_calling=False.
        for content in chat.history:
            for part in content.parts:
                if part.function_call:
                    print(f"\n--- DEBUG: Model decided to call function ---")
                    print(f"    Function: {part.function_call.name}")
                    print(f"    Args: {json.dumps(part.function_call.args, indent=2)}")
                elif part.function_response:
                    print(f"--- DEBUG: Function response received ---")
                    print(f"    From: {part.function_response.name}")
                    print(f"    Result: {json.dumps(part.function_response.response, indent=2)}")
        # --- End Debugging/Observing ---

        # Print the final text response from the model
        print(f"Chatbot: {response.text}")

    except Exception as e:
        print(f"Chatbot: An error occurred: {e}")
        print("Chatbot: Please try again or rephrase your request.")

print("\nChatbot: Goodbye!")
