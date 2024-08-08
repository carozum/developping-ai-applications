from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]


# Set your API key
client = OpenAI(api_key=openai_api_key)

messages1 = [{
    "role": "user",
    "content": "Please write down 5 trees with their scientific names in Json format"}]
messages2 = [
    {"role": "user", "content": "I have these notes with book titles and authors: New releases this week! The Beholders by Hester Musson, The Mystery Guest by Nita Prose. Please organize the titles and authors in a json file."}]

# specify the expected format json both in the prompt and in the response_format parameter of the OpenAI API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=150,
    messages=messages2,
    response_format={'type': "json_object"}
)

#  Extract and print the assistant's text response
print(response.choices[0].message.content)
