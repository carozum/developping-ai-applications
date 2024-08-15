"""
Parallel function calling with multiple functions

The default behavior (tool_choice: "auto") is for the model to decide on its own whether to call a function and if so which function to call.

To force the model to call a specific function set the tool_choice parameter with a specific function name. 

You can also force the model to generate a user-facing message by setting tool_choice: "none".
"""

from dotenv import find_dotenv, load_dotenv
import os
import json
from openai import OpenAI
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

# Set your API key
client = OpenAI(api_key=openai_api_key)

# set the model
model = "gpt-4o"

# Simplified weather data
WEATHER_DATA = {
    "tokyo": {"temperature": "10", "unit": "celsius"},
    "san francisco": {"temperature": "72", "unit": "fahrenheit"},
    "paris": {"temperature": "22", "unit": "celsius"}
}

# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}


def get_current_weather(location, unit=None):
    """Get the current weather for a given location"""
    print(
        f"get_current_weather called with location: {location}, unit: {unit}")
    location_lower = location.lower()

    for key in WEATHER_DATA:
        if key in location_lower:
            print(f"Weather data found for {key}")
            weather = WEATHER_DATA[key]
            return json.dumps({
                "location": location,
                "temperature": weather["temperature"],
                "unit": unit if unit else weather["unit"]
            })

    print(f"No weather data found for {location_lower}")
    return json.dumps({"location": location, "temperature": "unknown"})


def get_current_time(location):
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")
    location_lower = location.lower()

    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")
            current_time = datetime.now(
                ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })

    print(f"No timezone data found for {location_lower}")
    return json.dumps({"location": location, "current_time": "unknown"})


def run_conversation(input):
    # Initial user message
    messages = [
        {"role": "user", "content": input}]

    # Define the functions for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the functions
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # 1. Process the model's response to know if a function is needed or not and which one
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")
    print(response_message)

    # 2. Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            print(f"Function call: {function_name}")
            print(f"Function arguments: {function_args}")

            if function_name == "get_current_weather":
                function_response = get_current_weather(
                    location=function_args.get("location"),
                    unit=function_args.get("unit")
                )
            elif function_name == "get_current_time":
                function_response = get_current_time(
                    location=function_args.get("location")
                )
            else:
                function_response = json.dumps({"error": "Unknown function"})

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
    else:
        print("No tool calls were made by the model.")

    # 3. Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return final_response.choices[0].message.content


# Run the conversation and print the result
input = "What's the weather and current time in San Francisco, Tokyo, and Paris?"
print(run_conversation(input))

input2 = "what is adaptative AI in 150 tokens ?"
print(run_conversation(input2))

"""The JSON response might not always be valid so you need to add additional logic to your code to be able to handle errors. For some use cases you may find you need to use fine-tuning to improve function calling performance. https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning-functions """
