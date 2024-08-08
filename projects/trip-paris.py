from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(
    api_key=openai_api_key
)

conversation = [
    {"role": "system", "content": "You are a guide in Paris explaining tourist what to see in Paris and how to go to different points of interest. You are always polite and kind. You answer in english or in any other language if the user asks you for.  "},
    {"role": "user",
        "content": "How far away is the Louvre from the Eiffel Tower (in miles) if you are driving?"},
    {"role": "user", "content": "Where is the Arc de Triomphe?"},
    {"role": "user", "content": "What are the must-see artworks at the Louvre Museum?"},
]
