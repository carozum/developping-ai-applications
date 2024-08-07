from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(
    api_key=openai_api_key
)

# read a file and store it in a binary format
audio_file = open(
    "api-openai-endpoints/French-testimonial.mp3",
    "rb")

response = client.audio.translations.create(
    model="whisper-1",
    file=audio_file,
    prompt="about a french team of research on solar energy in connecticut"
)

print(response.text)
