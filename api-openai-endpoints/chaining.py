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

# Create a transcription request using audio_file
response = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file  # audio file to transcribe
)

transcript = response.text


# Create a request to the API to identify the language spoken
chat_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{'role': "user",
               'content': "Give me the name of the language used in the transcript: " + transcript}]

)
print(chat_response.choices[0].message.content)

# Create a request to the API to summarize the transcript into bullet points
chat_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {'role': 'user', 'content': 'Can you summarize  the transcript into concise bullet points' + transcript}
    ]
)
print(chat_response.choices[0].message.content)
