from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

########################################################
# Prompts

prompt1 = "Simply and concisely, explain why learning about the OpenAI API is important for developers."

job_title = "developer AI"

prompt2 = f"I work as a {job_title}. Give me three concise suggestions for tasks that could be automated with the OpenAI API."

prompt3 = "In two sentences, how can the OpenAI API be used to upskill myself?"

##############################################################
# interogating openai api completion end point (single turn)
# question answering

client = OpenAI(api_key=openai_api_key)

response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    # Write your prompt
    prompt=prompt1,
    max_tokens=200
)

print(response.choices[0].text)
