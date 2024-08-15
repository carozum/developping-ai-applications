##############################################################
# use case 2 : applied a custom function
# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling

from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI
import json
from zoneinfo import ZoneInfo
from datetime import datetime

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

model = "gpt-4o"

# Set your API key
client = OpenAI(api_key=openai_api_key)


####################################################
# define the function


# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}


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


######################################################
# run conversation


# Initial user message
# Single function call
messages1 = [
    {"role": "user", "content": "What's the current time in San Francisco"}]
messages2 = [
    {"role": "user", "content": "What's generative AI?"}]
# messages = [{"role": "user", "content": "What's the current time in San Francisco, Tokyo, and Paris?"}] # Parallel function call with a single tool/function defined


def run_conversation(messages):

    # Define the function for the model
    tools = [
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

    # First API call: Ask the model to use the function
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=150,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")
    print(response_message)

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "get_current_time":
                function_args = json.loads(tool_call.function.arguments)
                print(f"Function arguments: {function_args}")
                time_response = get_current_time(
                    location=function_args.get("location")
                )
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_current_time",
                    "content": time_response,
                })
    else:
        print("No tool calls were made by the model.")

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return final_response.choices[0].message.content


###################################################################
# conversation using tool_calls
# Run the conversation and print the result
print(run_conversation(messages1))


"""Model's response:
ChatCompletionMessage(content=None, refusal=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_p74gJw1LIVAaoQuZXKH9TRAJ', function=Function(arguments='{"location":"San Francisco"}', name='get_current_time'), type='function')])
Function arguments: {'location': 'San Francisco'}
get_current_time called with location: San Francisco
Timezone found for san francisco
The current time in San Francisco is 5:23 AM.
    """

##################################################################
# conversation without tool_calls

print(run_conversation(messages2))

"""Model's response:
ChatCompletionMessage(content='Generative AI refers to a type of artificial intelligence that is capable of generating new content, such as text, images, audio, and even video. Unlike traditional AI that focuses on recognizing patterns and making predictions based on existing data, generative AI creates new data that did not exist before. This is achieved through sophisticated algorithms and models, particularly those involving deep learning and neural networks.\n\nSome common examples of generative AI include:\n\n1. **Text Generation**: Models like GPT-3 (Generative Pre-trained Transformer 3) that can write essays, answer questions, create poetry, and even engage in human-like conversations.\n2. **Image Creation**: Tools like DeepArt and GANs (Generative Adversarial Networks) that can', refusal=None, role='assistant', function_call=None, tool_calls=None)
No tool calls were made by the model.
generate realistic images or transform one image style into another.
3. **Audio Generation**: AI systems that can create music, generate speech, or even mimic a specific person's voice with high accuracy.
4. **Video Generation**: AI that can produce new video content, including deepfakes where the appearance and voice of real individuals are convincingly altered to say or do things they never actually did.

Generative AI works by learning from a vast amount of data and then using what it has learned to produce new, similar data. For instance, a model trained on thousands of images of cats can generate entirely new images that are recognizably cats, even if no actual photograph matches exactly.

A notable application of generative AI is in creative industries where it can assist artists, musicians, and writers in the creation process, often suggesting novel ideas or automating routine tasks. However, it also raises ethical and societal concerns, such as the potential for misuse in spreading misinformation, creating fake content, and infringing on intellectual property. 

Because of their expansive capabilities, generative AI models often require significant computational resources and careful handling to ensure they're used responsibly and ethically."""
