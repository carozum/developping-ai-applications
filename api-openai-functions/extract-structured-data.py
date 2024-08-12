from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

# Set your API key
client = OpenAI(api_key=openai_api_key)

input = """Role: Engineering Manager AI - Conversational AI
Location: Remote/ Germany
Salary: upto €110,000

Our goal is to create the most personalized, effective, and inspiring educational journey online and through our sales channels, helping students worldwide achieve personal growth.

Responsibilities:
Design, implement, and refine agent-based systems for personalized content creation and conversational AI.
Lead a diverse team of engineers across AI and Data by example with hands-on engineering contributions.
Contribute to the development of a robust training, data, and MLOps infrastructure for cutting-edge AI projects.
Collaborate with business stakeholders to convert business objectives into AI-driven, impactful solutions.

Your Profile:
Minimum of 4 years’ experience in Deep/Machine Learning Engineering, specializing in NLP or LLMs.
Experience in managing and mentoring groups of individual contributors."""
messages = [{"role": "user", "content": input}]

model = "gpt-3.5-turbo"

function_definition = [{
    'type': "function",  # for our own designed functions
    'function': {  # information about the function
            "name": "extract_job_info",
            "description": "Get the job information from the body of the input text",
            "parameters": {
                # each key is a key that will be included in the resulting JSON schema
                "type": "object",
                "properties": {
                    "job": {"type": "string", "description": "Job Title"},
                    "location": {'type': "string", "description": "Office location"}
                }
            }
    }
}]


def get_response_with_tools(model, messages, function_definition):
    # Create a request to the Chat Completions endpoint
    response = client.chat.completions.create(
        model=model,
        max_tokens=150,
        messages=messages,
        tools=function_definition
    )
    return response.choices[0].message.tool_calls[0].function.arguments

# when using function calling, the response will be nested in tool_calls[0].function.arguments


print(get_response_with_tools(model, messages, function_definition))
# {"job":"Engineering Manager AI - Conversational AI","location":"Remote/ Germany"}


###################################################################

message_listing = [{'role': 'system', 'content': "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}, {
    'role': 'user', 'content': 'Step into this beautiful two-story, single-family home located in Springfield, USA, priced at $350,000. This charming property features 4 bedrooms, 2.5 bathrooms, a spacious living room with a cozy fireplace, a modern kitchen with stainless steel appliances, and a large backyard perfect for family gatherings. The master bedroom includes an en-suite bathroom and a walk-in closet. Enjoy the convenience of an attached two-car garage and a recently updated HVAC system. Located near top-rated schools, parks, and shopping centers, this home is ideal for families looking for comfort and convenience.'}]

function_definition = [{
    'type': 'function',
    'function': {
        'name': 'real_estate_info',
        'description': 'Get the information about homes for sale from the body of the input text',
        'parameters': {
            'type': 'object',
            'properties': {
                'home type': {'type': 'string', 'description': 'Home type'},
                'location': {'type': 'string', 'description': 'Location'},
                'price': {'type': 'integer', 'description': 'Price'},
                'bedrooms': {'type': 'integer', 'description': 'Number of bedrooms'}
            }
        }
    }
}]

print(get_response_with_tools(model, message_listing, function_definition))

# {"home type": "single-family", "location": "Springfield, USA","price": 350000, "bedrooms": 4}

##################################################################
messages = [{'role': 'system', 'content': "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}, {'role': 'user', 'content': '\nA. M. Turing (1950) Computing Machinery and Intelligence. Mind 49: 433-460.\nCOMPUTING MACHINERY AND INTELLIGENCE\nBy A. M. Turing\n1. The Imitation Game\nI propose to consider the question, "Can machines think?" This should begin with\ndefinitions of the meaning of the terms "machine" and "think." The definitions might be\nframed so as to reflect so far as possible the normal use of the words, but this attitude is\ndangerous, If the meaning of the words "machine" and "think" are to be found by\nexamining how they are commonly used it is difficult to escape the conclusion that the\nmeaning and the answer to the question, "Can machines think?" is to be sought in a\nstatistical survey such as a Gallup poll. But this is absurd. Instead of attempting such a\ndefinition I shall replace the question by another, which is closely related to it and is\nexpressed in relatively unambiguous words.\nThe new form of the problem can be described in terms of a game which we call the\n\'imitation game." It is played with three people, a man (A), a woman (B), and an\ninterrogator (C) who may be of either sex. The interrogator stays in a room apart front the\nother two. The object of the game for the interrogator is to determine which of the other\ntwo is the man and which is the woman. He knows them by labels X and Y, and at the\nend of the game he says either "X is A and Y is B" or "X is B and Y is A." The\ninterrogator is allowed to put questions to A and B thus:\nC: Will X please tell me the length of his or her hair?\nNow suppose X is actually A, then A must answer. It is A\'s object in the game to try and\ncause C to make the wrong identification. His answer might therefore be:\n"My hair is shingled, and the longest strands are about nine inches long."\nIn order that tones of voice may not help the interrogator the answers should be written,\nor better still, typewritten. The ideal arrangement is to have a teleprinter communicating\nbetween the two rooms. Alternatively the question and answers can be repeated by an\nintermediary. The object of the game for the third player (B) is to help the interrogator.\nThe best strategy for her is probably to give truthful answers. She can add such things as\n"I am the woman, don\'t listen to him!" to her answers, but it will avail nothing as the man\ncan make similar remarks.\nWe now ask the question, "What will happen when a machine takes the part of A in this\ngame?" Will the interrogator decide wrongly as often when the game is played like this as\nhe does when the game is played between a man and a woman? These questions replace\nour original, "Can machines think?\n                 '}]

function_definition = [{
    'type': 'function',
    'function': {
        'name': 'extract_review_info',
        'description': 'Extract the title and year of publication from research papers.',
        'parameters': {
            'type': 'object',
            'properties': {
                'title': {'type': 'string', 'description': 'the title'},
                'year': {'type': 'string', 'description': 'date of publication'}
            }
        }
    }
}]

print(get_response_with_tools(model, messages, function_definition))
# {"title":"Computing Machinery and Intelligence","year":"1950"}


##############################################################
messages = [{'role': 'system', 'content': "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}, {'role': 'user',
                                                                                                                                                                      'content': "\nI recently purchased the TechCorp ProMax and I'm absolutely in love with its powerful processor. However, I think they could really improve the product by deciding to offer more color options.\n"}]

function_definition = [{
    'type': 'function',
    'function': {
        'name': 'extract_sentiment_and_product_features',
        'description': 'Extract sentiment and product features from reviews',
        'parameters': {
            'type': 'object',
            'properties': {
                'product': {'type': 'string', 'description': 'The product name'},
                'sentiment': {'type': 'string', 'description': 'The overall sentiment of the review'},
                'features': {'type': 'array', 'items': {'type': 'string'}, 'description': 'List of features mentioned in the review'},
                'suggestions': {'type': 'array', 'items': {'type': 'string'}, 'description': 'Suggestions for improvement'}
            }
        }
    }
}]
print(get_response_with_tools(model, messages, function_definition))
# {"product":"TechCorp ProMax","features":["powerful processor"],"suggestions":["offer more color options"]}
