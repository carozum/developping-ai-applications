from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(
    api_key=openai_api_key
)

input1 = "I could kill a hamburger"
input2 = "My favorite book is How to Kill a Mockingbird."

response = client.moderations.create(
    model="text-moderation-latest",
    input=input2
)
print(response.model_dump())


""" {
    'id': 'modr-9thJicWR1au53i0NIOZ49k7LsBxBi', 
    'model': 'text-moderation-007', 
    'results': [{
        'categories': {'harassment': False, 'harassment_threatening': False, 'hate': False, 'hate_threatening': False, 'self_harm': False, 'self_harm_instructions': False, 'self_harm_intent': False, 'sexual': False, 'sexual_minors': False, 'violence': False, 'violence_graphic': False, 'self-harm': False, 'sexual/minors': False, 'hate/threatening': False, 'violence/graphic': False, 'self-harm/intent': False, 'self-harm/instructions': False, 'harassment/threatening': False},
        'category_scores': {'harassment': 0.03256910294294357, 'harassment_threatening': 0.02063307724893093, 'hate': 0.00040756360976956785, 'hate_threatening': 8.966411405708641e-05, 'self_harm': 0.0007399782771244645, 'self_harm_instructions': 8.171325589501066e-07, 'self_harm_intent': 0.00022090923448558897, 'sexual': 6.245846452657133e-05, 'sexual_minors': 1.2626526313397335e-06, 'violence': 0.5198577642440796, 'violence_graphic': 0.0007369354134425521, 'self-harm': 0.0007399782771244645, 'sexual/minors': 1.2626526313397335e-06, 'hate/threatening': 8.966411405708641e-05, 'violence/graphic': 0.0007369354134425521, 'self-harm/intent': 0.00022090923448558897, 'self-harm/instructions': 8.171325589501066e-07, 'harassment/threatening': 0.02063307724893093}, 
        'flagged': False
        }]}"""
print(response.results[0].category_scores)
