"""
Parallel function calling with multiple functions

The default behavior (tool_choice: "auto") is for the model to decide on its own whether to call a function and if so which function to call.

To force the model to call a specific function set the tool_choice parameter with a specific function name. 

You can also force the model to generate a user-facing message by setting tool_choice: "none".

https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling
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

#######################################################################
# Let the model choose which function to apply


def run_conversation_auto(input):
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
        # default behavior, the model choose the function to use based on the message and function definitions
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
print(run_conversation_auto(input))

input2 = "what is adaptative AI in 150 tokens ?"
print(run_conversation_auto(input2))

"""The JSON response might not always be valid so you need to add additional logic to your code to be able to handle errors. For some use cases you may find you need to use fine-tuning to improve function calling performance. https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning-functions """


#######################################################################
# choose a function to apply

tool_choice = {
    'type': "function",
    'function': {'name': 'get_current_weather'}}


###################################################################
# second example

input = "\nI recently purchased the TechCorp ProMax and I'm absolutely in love with its powerful processor. However, I think they could really improve the product by deciding to offer more color options.\n"

model = "gpt-4o"


def get_response(model, input, function_definition):

    messages = [
        {'role': 'system', 'content': 'Apply both functions and return responses.'},
        {'role': 'user', 'content': input}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=function_definition
    )
    response_message = response.choices[0].message

    return response_message


function_definition = [
    {'type': 'function',
     'function': {
         'name': 'extract_sentiment_and_product_features',
         'parameters': {
             'type': 'object',
             'properties': {
                 'product': {'type': 'string', 'description': 'The product name'},
                 'sentiment': {'type': 'string', 'description': 'The overall sentiment of the review'},
                 'features': {'type': 'array', 'items': {'type': 'string'}, 'description': 'List of features mentioned in the review'},
                 'suggestions': {'type': 'array', 'items': {'type': 'string'}, 'description': 'Suggestions for improvement'}
             }
         }
     }
     }
]
# Append the second function
function_definition.append(
    {'type': 'function',
     'function': {
         'name': "reply_to_review",
         'description': "reply to the review",
         "parameters": {
             'type': 'object',
             'properties': {
                 'reply': {
                     'type': "string",
                     'description': "response to the review"}
             }
         }
     }
     })

response = get_response(model, input, function_definition)
for tool_call in response.tool_calls:

    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    if function_name == "extract_sentiment_and_product_features":
        function_response = f"Sentiment :  {function_args['sentiment']}"
    elif function_name == "reply_to_review":
        function_response = f"Reply: {function_args['reply']}"

    print(function_response)

""" 
{"product": "TechCorp ProMax", 
"sentiment": "positive", 
"features": ["powerful processor"], 
"suggestions": ["offer more color options"]}

{"reply": "Thank you for your feedback! We're thrilled to hear you love the powerful processor of the TechCorp ProMax. Your suggestion for more color options has been noted and will be passed along to our development team. We always strive to improve and your input is invaluable."}

Sentiment :  positive

Reply: Thank you for your positive feedback on the TechCorp ProMax! We're thrilled to hear that you love its powerful processor. Your suggestion to offer more color options is greatly appreciated and will be considered by our product team. Thank you for helping us improve!"""
