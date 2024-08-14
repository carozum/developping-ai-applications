from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

# Set your API key
client = OpenAI(api_key=openai_api_key)

input = """Role: Engineering Manager AI - Conversational AI
Location: Remote/ Germany
Salary: upto €110,000

Our goal is to create the most personalized, effective, and inspiring educational journey online and through our sales channels, helping students worldwide achieve personal growth.

Responsibilities:
Design, implement, and refine agent-based systems for personalized content creation and conversational AI.
Lead a diverse team of engineers across AI and Data by example with hands-on engineering contributions.
Contribute to the development of a robust training, data, and MLOps infrastructure for cutting-edge AI projects.
Collaborate with business stakeholders to convert business objectives into AI-driven, impactful solutions.

Your Profile:
Minimum of 4 years’ experience in Deep/Machine Learning Engineering, specializing in NLP or LLMs.
Experience in managing and mentoring groups of individual contributors."""
messages_system = [
    {'role': "system", "content": "Don't make assumptions about what values to plug into functions. Don't make up values to fill the response with.  "},
    {'role': "system", "content": "Ask for clarification if needed."},
]
message_1 = messages_system + [{"role": "user", "content": input}]

message_2 = messages_system + [{"role": "user",
                               "content": "What is the job about ?"}]


model = "gpt-3.5-turbo"

function_definition = [{
    'type': "function",  # for our own designed functions
    'function': {  # information about the function
            "name": "extract_job_info",
            "description": "Get the job information from the body of the input text",
            "parameters": {
                # each key is a key that will be included in the resulting JSON schema
                "type": "object",
                "properties": {
                    "job": {"type": "string", "description": "Job Title"},
                    "location": {'type': "string", "description": "Office location"}
                }
            }
    }
}]

# adding a new function to tools
function_definition.append({
    'type': 'function',
    'function': {
        'name': 'get_timezone',
        'description': 'Return the timezone corresponding to the location in the job advert',
        'parameters': {
            'type': 'object',
            'properties': {
                'timezone': {'type': 'string', 'description': 'Timezone'},
            },
            "required": ["timezone"]
        }
    }
})


def get_response_with_multiple_functions_auto(model, messages, function_definition):
    # Create a request to the Chat Completions endpoint
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=function_definition,
        tool_choice="auto",

    )
    n = len(response.choices[0].message.tool_calls)
    print(n)
    print([response.choices[0].message.tool_calls[i] for i in range(n)])
    return response.choices[0].message.content

# when using function calling, the response will be nested in tool_calls[0].function.arguments


print(get_response_with_multiple_functions_auto(
    model, message_1, function_definition))

# {"job":"Engineering Manager AI - Conversational AI","location":"Remote/ Germany"}

print(get_response_with_multiple_functions_auto(
    model, message_2, function_definition))


###############################################################

def get_response_with_multiple_functions_chosen(model, messages, function_definition):
    # Create a request to the Chat Completions endpoint
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=function_definition,
        tool_choice={
            'type': 'function',
            'function': {'name': 'get_timezone'}
        },

    )
    print(response.choices[0].message.tool_calls[0].function.arguments)

    return response.choices[0].message.content


print(get_response_with_multiple_functions_chosen(
    model, message_1, function_definition))
