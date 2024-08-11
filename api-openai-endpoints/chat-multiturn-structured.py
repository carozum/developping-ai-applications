""" 
https://platform.openai.com/docs/guides/structured-outputs/structured-outputs
structured output 
- custom structure
- json
- unstructured
Compatible with models GPT 3.5, GPT-4o and later, GPT-4o-mini...
"""

from pydantic import BaseModel
from dotenv import find_dotenv, load_dotenv
import os
from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError)

############################################################
# environment

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]


# Set your API key
client = OpenAI(api_key=openai_api_key)

############################################################
# messages
messages0 = [{
    "role": "user",
    "content": "Please write down 5 trees with their scientific names"}]
messages1 = [{
    "role": "user",
    "content": "Please write down 5 trees with their scientific names in Json format"}]
messages2 = [
    {"role": "user", "content": "I have these notes with book titles and authors: New releases this week! The Beholders by Hester Musson, The Mystery Guest by Nita Prose. Please organize the titles and authors in a json file."}]
messages3 = [
    {"role": "user", "content": "I have these notes with book titles and authors: New releases this week! The Beholders by Hester Musson, The Mystery Guest by Nita Prose. Please organize the titles and authors in the specified structure."}]

################################################################
# no structure for output


def get_response_not_structured(model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=prompt,
    )
    return response.choices[0].message.content


#  Extract and print the assistant's text response
print(get_response_not_structured("gpt-3.5-turbo", messages0))

"""
1. Oak tree - Quercus
2. Maple tree - Acer
3. Pine tree - Pinus
4. Birch tree - Betula
5. Elm tree - Ulmus
"""

################################################################
# output JSON - specify the expected format json both in the prompt AND in the response_format parameter of the OpenAI API call


def get_response_json(model, messages):
    response = client.chat.completions.create(
        model=model,
        max_tokens=150,
        messages=[
            {"role": "system", "content": "you return data as a Json"}] + messages,
        response_format={'type': "json_object"}
    )
    return response.choices[0].message.content


#  Extract and print the assistant's text response
print(get_response_json("gpt-3.5-turbo", messages2))

"""
{
  "books": [
    {
      "title": "The Beholders",
      "author": "Hester Musson"
    },
    {
      "title": "The Mystery Guest",
      "author": "Nita Prose"
    }
  ]
}"""

################################################################
# output custom structure


class Step(BaseModel):
    explanation: str
    output: str


class MathResponse(BaseModel):
    steps: list[Step]
    final_answer: str


client = OpenAI()

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "solve 8x + 31 = 2"},
    ],
    response_format=MathResponse,
)

message = completion.choices[0].message
if message.parsed:
    print(message.parsed.steps)
    print(message.parsed.final_answer)
else:
    print(message.refusal)


#########################################################

# pip install --upgrade openai

client = OpenAI()


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed
print(event)
