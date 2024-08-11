from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)
from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

# Set your API key
client = OpenAI(
    api_key=openai_api_key,
    organization="org-w44aJlvsbRCs1gg6DQzyQ9BC")


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_response(model, message):
    response = client.chat.completions.create(
        model=model,
        messages=message,
        response_format={'type': 'json_object'}
    )
    return response.choices[0].message.content


"""In this example, we are asking the API to return the capital city for each of the countries given, through a list of dictionaries passed to the API. Notice that in this case we have specified precise instructions as the system message in order to get a full answer with all three responses."""

countries = ["USA", "France", "China"]
message = [
    {
        "role": "user",
        "content": """You are given a series of countries and are asked to return the country and capital city. Provide each of the questions with and answer in the response as separate content in json format"""
    }
]

[message.append({"role": "user", "content": country}) for country in countries]

print(message)
"""[{'role': 'user', 'content': 'You are given a series of countries and are asked to return the country and capital city. Provide each of the questions with and answer in the response as separate content.'}, {'role': 'user', 'content': 'USA'}, {'role': 'user', 'content': 'France'}, {'role': 'user', 'content': 'China'}]"""

print(get_response("gpt-4o", message))
