from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

########################################################
# Prompts

# content generation : question and answer
prompt1 = "Simply and concisely, explain why learning about the OpenAI API is important for developers."

job_title = "developer AI"

prompt2 = f"I work as a {job_title}. Give me three concise suggestions for tasks that could be automated with the OpenAI API."

prompt3 = "In two sentences, how can the OpenAI API be used to upskill myself?"

# text transformation : find and replace
# max_tokens 100, temperature 100
prompt4 = """Replace car with plane and adjust phrase:
A car is a vehicle that is typically powered by an internal combustion engine or an electric motor. It has four wheels, and is designed to carry passengers and/or cargo on roads or highways. Cars have become a ubiquitous part of modern society, and are used for a wide variety of purposes, such as commuting, travel, and transportation of goods. Cars are often associated with freedom, independence, and mobility."""

# text transformation : summarization
# max_tokens 400, temperature 0
prompt5 = """Summarize the following text into two concise bullet points:
Investment refers to the act of committing money or capital to an enterprise with the expectation of obtaining an added income or profit in return. There are a variety of investment options available, including stocks, bonds, mutual funds, real estate, precious metals, and currencies. Making an investment decision requires careful analysis, assessment of risk, and evaluation of potential rewards. Good investments have the ability to produce high returns over the long term while minimizing risk. Diversification of investment portfolios reduces risk exposure. Investment can be a valuable tool for building wealth, generating income, and achieving financial security. It is important to be diligent and informed when investing to avoid losses."""

# content generation
# max_tokens 100, temperature 1.5
prompt6 = "generate a catchy slogan for a new restaurant"

##############################################################
# interogating openai api completion end point (single turn)
# question answering

client = OpenAI(
    api_key=openai_api_key,
    organization="org-w44aJlvsbRCs1gg6DQzyQ9BC")

# request to the completions endpoint (single turn)
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    # Write your prompt
    prompt=prompt6,
    temperature=1.5,
    max_tokens=100,
    n=2
)

# print(response)  # a completion object
# print(response.model_dump())  # convert to dictionary
for i in range(2):
    # text of the first response
    print(f"response {i} : {response.choices[i].text}")
