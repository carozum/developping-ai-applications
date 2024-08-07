from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]


# instructions
# question answer
instruction1 = "What is the difference between a for loop and a while loop?"

# code explanation
instruction2 = """Explain what this Python code does in one sentence:
import numpy as np

heights_dict = {"Mark": 1.76, "Steve": 1.88, "Adnan": 1.73}
heights = heights_dict.values()
print(np.mean(heights))
"""


# Set your API key
client = OpenAI(api_key=openai_api_key)


# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=150,
    messages=[
        {"role": "system", "content": "a developer assistant in python"},
        {"role": "user", "content": instruction2}
    ],
)

#  Extract and print the assistant's text response
print(response.choices[0].message.content)
