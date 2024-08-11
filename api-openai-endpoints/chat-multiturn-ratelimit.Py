import tiktoken
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)
from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

##########################################################
# 0. set the environment

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

# Set your API key
client = OpenAI(
    api_key=openai_api_key,
    organization="org-w44aJlvsbRCs1gg6DQzyQ9BC")

# set the model
model = "gpt-4o"


###########################################################
# 1. Adding a retry decorator to the different functions


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_response_json(model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "you return data as a Json"}] + prompt,
        response_format={'type': 'json_object'}
    )
    return response.choices[0].message.content


print(get_response_json(model, [{"role": "user",
      "content": "List ten holiday destinations, in the format of a Json"}]))


def get_response(model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=prompt
    )
    return response.choices[0].message.content


######################################################
# 2. batching in one request multiple queries
"""In this example, we are asking the API to return the capital city for each of the countries given, through a list of dictionaries passed to the API. Notice that in this case we have specified precise instructions as the system message in order to get a full answer with all three responses."""

countries = ["USA", "France", "China"]
message = [
    {
        "role": "system",
        "content": """You are given a series of countries and are asked to return the country and capital city. Provide each of the questions with and answer in the response as separate content in json format"""
    }
]

[message.append({"role": "user", "content": country}) for country in countries]

print(message)
"""[{'role': 'user', 'content': 'You are given a series of countries and are asked to return the country and capital city. Provide each of the questions with and answer in the response as separate content in json format.'}, {'role': 'user', 'content': 'USA'}, {'role': 'user', 'content': 'France'}, {'role': 'user', 'content': 'China'}]"""

print(get_response_json(model, message))


"""You are developing a fitness application to track running and cycling training, but find out that all your customers' distances have been measured in kilometers, and you'd like to have them also converted to miles.

You decide to use the OpenAI API to send requests for each measurement, but want to avoid using a for loop that would send too many requests. You decide to send the requests in batches, specifying a system message that asks to convert each of the measurements from kilometers to miles and present the results in a table containing both the original and converted measurements.

The measurements list (containing a list of floats) and the get_response() function have already been imported"""

measurements = [5.2, 6.3, 3.7]
messages = []
# Provide a system message and user messages to send the batch
messages.append(
    {'role': 'system', "content": """You are given a series of measurements and are asked to convert each of the measurements from kilometers to miles and present the results in a table containing both the original and converted measurements"""}
)
# Append measurements to the message
[messages.append({"role": "user", "content": str(measure)})
 for measure in measurements]

response = get_response("gpt-4o", messages)
print(response)
"""
messages = [{'role': 'system', 'content': 'You are given a series of measurements and are asks to convert each of the measurements from kilometers to miles and present the results in a table containing both the original and converted measurements'}, {'role': 'user', 'content': 5.2}, {'role': 'user', 'content': 6.3}, {'role': 'user', 'content': 3.7}]"""

response = get_response_json(model, messages)
print(response)


#######################################################
# 3. Reducing the number of tokens

# Use tiktoken to create the encoding for your model
encoding = tiktoken.encoding_for_model(model)

prompt = "Tokens can be full words, or groups of characters commonly grouped together: tokenization. "
num_tokens = len(encoding.encode(prompt))
print(num_tokens)


input_message = {"role": "user",
                 "content": "I'd like to buy a shirt and a jacket. Can you suggest two color pairings for these items?"}

# Check for the number of tokens
num_tokens = len(encoding.encode(input_message['content']))

# Run the chat completions function and print the response
if num_tokens <= 100:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[input_message])
    print(response.choices[0].message.content)
else:
    print("Message exceeds token limit")
