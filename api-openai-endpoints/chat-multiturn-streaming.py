from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

# Set your API key
client = OpenAI(api_key=openai_api_key)


stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user",
               "content": "can you tell me what monument to visite in Almeria, Spain?"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
