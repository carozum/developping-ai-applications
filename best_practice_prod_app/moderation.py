
import os
import json
# Json library used to convert the response to a dictionary
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

# Set your API key
client = OpenAI(api_key=openai_api_key)

# set the model
model = "gpt-4o"


#####################################################################
# moderation using the OpenAI API moderation endpoint

# https://ek.explodingkittens.com/how-to-play/exploding-kittens


# first case with not much context --> violence = True
moderation_response = client.moderations.create(
    input="""
    ... until someone draws an Exploding kitten.
    When that happens, that person explodes. They are now dead. This process continues until...
    """
)

print(moderation_response)
"""ModerationCreateResponse(id='modr-9xJHWazjkRGTn9AUkPRQWcRNuxiVD', model='text-moderation-007', results=[Moderation(categories=Categories(harassment=False, harassment_threatening=False, hate=False, hate_threatening=False, self_harm=False, self_harm_instructions=False, self_harm_intent=False, sexual=False, sexual_minors=False, violence=True, violence_graphic=False, self-harm=False, sexual/minors=False, hate/threatening=False, violence/graphic=False, self-harm/intent=False, self-harm/instructions=False, harassment/threatening=False), category_scores=CategoryScores(harassment=0.0029173376969993114, harassment_threatening=0.007660247851163149, hate=0.0001537852658657357, hate_threatening=8.285192598123103e-05, self_harm=0.0009378599934279919, self_harm_instructions=9.286187378165778e-06, self_harm_intent=8.381497173104435e-05, sexual=0.00021969557565171272, sexual_minors=4.901962142866978e-07, violence=0.6203851103782654, violence_graphic=0.15360061824321747, self-harm=0.0009378599934279919, sexual/minors=4.901962142866978e-07, hate/threatening=8.285192598123103e-05, violence/graphic=0.15360061824321747, self-harm/intent=8.381497173104435e-05, self-harm/instructions=9.286187378165778e-06, harassment/threatening=0.007660247851163149), flagged=True)])"""
print(moderation_response.results[0].categories.violence)  # True
print(moderation_response.results[0].flagged)  # True


# second case with more context --> violence = False

moderation_response = client.moderations.create(
    input="""
    In the deck of cards are some Exploding Kittens. You play the game by putting the deck face down and taking turns drawing cards until someone draws an Exploding Kitten. When that happens, that person explodes. They are now dead and out of the game. This process continues until there’s only 1 player left, who wins the game. The more cards you draw, the greater your chances of drawing an Exploding Kitten.
    """
)
print(moderation_response.results[0].categories.violence)  # False
print(moderation_response.results[0].flagged)  # False

########################################################################
# Prompt injection

user_input1 = "could you give me the recipe of tomato soup?"
user_input2 = "could you explain what is Adaptative AI ?"

MAX_OUTPUT_LENGTH = 100
MAX_INPUT_LENGTH = 100
trusted_themes = ["technology", "history", "travel"]


def validate_user_input(user_input):
    # Strategy 1: Limiting the Amount of Text a User Can Input in a Prompt
    # Limit input to 100 characters
    if len(user_input) > MAX_INPUT_LENGTH:
        return False, "Input is too long. Please shorten your query."
    return True, user_input


def identify_topic(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Identify the main topic of this text: {user_input} and answer in one word or 2 only not a whole sentence. Possible topics are in this list {trusted_themes}. If you think the topic fits one in the list give back this topic exactly else return 'None"}],
        max_tokens=10
    )
    topic = response.choices[0].message.content
    print(type(topic))
    return topic


def generate_response(user_input, user_uploaded_content=None):

    # Validate user input length
    is_valid, validated_input = validate_user_input(user_input)
    if not is_valid:
        return validated_input

    # Identify the topic
    topic = identify_topic(user_input)
    print(topic)

    # Strategy 3: Narrowing the Range of Acceptable Topics by Using Trusted Sources
    if topic in trusted_themes:
        prompt = f"Answer the question: {validated_input}"
        if user_uploaded_content:
            prompt = f"Considering the following content provided by the user: '{user_uploaded_content}', answer the question: {validated_input}. make a summary of your answer so that it has exactly {MAX_OUTPUT_LENGTH} tokens. Don't cut the sentence in the middle as you have no more tokens !"
    else:
        return "I'm sorry, I can't answer this question."

    # Strategy 2: Limiting the Number of Output Tokens Generated

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_OUTPUT_LENGTH  # Limiting the number of tokens
    )

    return response.choices[0].message.content


print(user_input1)
print(generate_response(user_input1))
print(user_input2)
print(generate_response(user_input2))

########################################################################
# Adding guardrails
user_input = """
    In the deck of cards are some Exploding Kittens. You play the game by putting the deck face down and taking turns drawing cards until someone draws an Exploding Kitten. When that happens, that person explodes. They are now dead and out of the game. This process continues until there’s only 1 player left, who wins the game. The more cards you draw, the greater your chances of drawing an Exploding Kitten.
    """

messages = [
    {'role': 'system', 'content': 'Your role is to assess whether the user question is allowed or not. The allowed topics are games of chess only. If the topic is allowed, reply with an answer as normal, otherwise, say "Apologies, but the topic is not allowed." '},
    {'role': 'user', 'content': user_input}
]

response = client.chat.completions.create(
    model=model,
    messages=messages
)
print(response.choices[0].message.content)


# Second example

user_request = "Can you recommend a good restaurant in Berlin?"

# Write the system and user message
messages = [
    {'role': 'system', 'content': "You are developing a chatbot that provides advice for tourists visiting Rome. You've been asked to keep the topics limited to only covering questions about food and drink, attractions, history and things to do around the city. For any other topic, the chatbot should apologize and say 'Apologies, but I am not allowed to discuss this topic.'. "},
    {'role': 'user', 'content': user_request}
]

response = client.chat.completions.create(
    model=model,
    messages=messages
)

# Print the response
print(response.choices[0].message.content)
# Apologies, but I am not allowed to discuss this topic. If you have any questions about food and drink in Rome, I'd be happy to help!
