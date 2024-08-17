# https://api.artic.edu/docs/#quickstart

import requests
import os
import json
# Json library used to convert the response to a dictionary
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

# Set your API key
client = OpenAI(api_key=openai_api_key)

# set the model
model = "gpt-4o"


def postprocess_response(response):
    # Check that the response has been produced using function calling
    if response.choices[0].finish_reason == 'tool_calls':
        function_call = response.choices[0].message.tool_calls[0].function
        if function_call.name == "get_airport_info":
            code = json.loads(function_call.arguments)["airport_code"]
            airport_info = get_airport_info(code)
            if airport_info:
                return airport_info
            else:
                print(
                    "Apologies, I couldn't find any airport.")
        elif function_call.name == "get_artwork":
            artwork_keyword = json.loads(function_call.arguments)[
                "artwork_keyword"]
            artwork = get_artwork((artwork_keyword))
            if artwork:
                print(
                    f"Here are some recommendations: {[i['title'] for i in json.loads(artwork)['data']]}")
            else:
                print("Apologies, could not make recommendations")

        else:
            print("Apologies, I couldn't find any airport or artwork.")
    else:
        print("I am sorry, but I could not understand your request.")


def get_response(model, messages, function_definition):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=function_definition,
    )
    return postprocess_response(response)


def print_response(response):
    print(postprocess_response(response))

# package the external API call as a function that we are going to call


def get_artwork(keyword):
    url = "https://api.artic.edu/api/v1/artworks/search"
    querystring = {"q": keyword}
    response = requests.request("GET", url, params=querystring)
    return response.text


# print(get_artwork("cat"))


def get_airport_info(airport_code):
    url = "https://api.aviationapi.com/v1/airports"
    querystring = {"apt": airport_code}
    response = requests.request("GET", url, params=querystring)
    return response.text


# print(get_airport_info("JFK"))

#################################################
# example 1

input = "I don't have much time to visit the museum and I would like some recommendations. I like the seaside and quiet places"
messages = [
    {"role": "system", "content": "You are an AI assistant, a specialist in history of art. You should interpret the user prompt, and based on it extract one keyword for recommending artwork related tot their preference"},
    {"role": "user", "content": input}
]
function_definition = [{
    "type": "function",
    "function": {
        "name": "get_artwork",
        "description": "interpret the user prompt, and based on it extract one keyword ",
        "parameters": {
            "type": "object",
            "properties": {
                "artwork_keyword": {
                    "type": "string",
                    "description": "The keyword to be passed to the get_artwork function"
                }
            }
        },
        "result": {"type": "string"},
        "required": ["artwork_keyword"]
    }
}]


response = get_response(model, messages, function_definition)
print(response)


##################################################
# Example 2

# import inspect
# print(inspect.getsource(function_name))

messages = [
    {
        "role": "system",
        "content": "You are an AI assistant, an aviation specialist. You should interpret the user prompt, and based on it extract an airport code corresponding to their message."
    },
    {"role": "user", "content": "I'm planning to land a plane in JFK airport in New York and would like to have the corresponding information."}
]

# Define the function to pass to tools
function_definition = [
    {"type": "function",
     "function": {
             "name": "get_airport_info",
             "description": "Return a matching airport code",
         "parameters": {
             "type": "object",
             "properties": {"airport_code": {"type": "string", "description": "the code to be passed to the get_airport_info function"}}},
         "result": {"type": "string"}}}]

response = get_response(model, messages, function_definition)
print(response)

########################################################################
# example 3
