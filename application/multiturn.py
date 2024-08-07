from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]


# instructions
# question answer
instruction1 = "What is the difference between a for loop and a while loop?"
messages1 = [
    {"role": "system", "content": "a developer assistant in python"},
    {"role": "user", "content": instruction1}
],

# code explanation
instruction2 = """Explain what this Python code does in one sentence:
import numpy as np

heights_dict = {"Mark": 1.76, "Steve": 1.88, "Adnan": 1.73}
heights = heights_dict.values()
print(np.mean(heights))
"""
messages2 = [
    {"role": "system", "content": "a developer assistant in python"},
    {"role": "user", "content": instruction2}
],

# Add a user and assistant message for in-context learning (one shot prompting)
messages3 = [
    {"role": "system", "content": "You are a helpful Python programming tutor."},
    {"role": "user", "content": "Explain what the min() function does."},
    {"role": "assistant",
        "content": "The min() function returns the smallest item from an iterable."},
    {"role": "user", "content": "Explain what the type() function does."}
]


# Set your API key
client = OpenAI(api_key=openai_api_key)


# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=150,
    messages=messages3,
)

#  Extract and print the assistant's text response
print(response.choices[0].message.content)


# AI chatbot

messages = [{"role": "system", "content": "You are a helpful math tutor."}]
user_msgs = ["Explain what pi is.", "Summarize this in two bullet points."]

for q in user_msgs:
    print("User: ", q)

    # Create a dictionary for the user message from q and append to messages
    user_dict = {"role": "user", "content": q}
    messages.append(user_dict)

    # Create the API request
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100
    )

    # Convert the assistant's message to a dict and append to messages
    assistant_dict = {"role": "assistant",
                      "content": response.choices[0].message.content}
    messages.append(assistant_dict)
    print("Assistant: ", response.choices[0].message.content, "\n")
