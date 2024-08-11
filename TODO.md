###########################################################
# revoir le mail de ce que veut le client


#######################################################
# suivi des nouveautés

Search GPT

custom structure for output


###########################################################
# relire la documentation d'OpenAI / Azure OpenAI...

https://learn.microsoft.com/en-us/azure/ai-services/openai/?view=rest-azureopenai-2024-05-01-preview 
https://platform.openai.com/docs/api-reference/ : quickstart
- pour identifier les endpoints et comment s'en servir
- pour identifier tous les paramètres des appels API et leur impact/intérêt

## Faire une liste des endpoints existant dans Open AI ou Azure Open AI 
Voir pour l'upload si on peut se servir du file API
Voir si on peut utiliser l'assistant APi ou si encore en version beta

## paramètres
Ajout de plusieurs réponses au chat gpt, 
ajuster température, top-p max-tokens et n pour avoir des réponses différentes

## format des réponses
- response_format={'type': "json_object"} + ajouter dans le prompt le format de la réponse
- custom format défini via des classes

### Stream, asynchronous
stream true dans le chat.completion

###########################################################
# errors handling
add try except block with error handling around the OpenAI API call (use specific errors relating to OpenAI)


###########################################################
# nouvelle API Azure OpenAI on your data
à explorer
https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?view=rest-azureopenai-2024-05-01-preview&tabs=python 

https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart?view=rest-azureopenai-2024-05-01-preview&tabs=command-line%2Cpython-new&pivots=programming-language-python 
--> voir comment se tenir à jour des nouveautés Azure ?

import os
import openai
import dotenv

dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID")

client = openai.AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",
)

completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "What are my available health plans?",
        },
    ],
    extra_body={
        "data_sources":[
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],
                    "index_name": os.environ["AZURE_AI_SEARCH_INDEX"],
                    "authentication": {
                        "type": "api_key",
                        "key": os.environ["AZURE_AI_SEARCH_API_KEY"],
                    }
                }
            }
        ],
    }
)

print(completion.model_dump_json(indent=2))

###########################################################
# modèles 

## GPT 4o mini
Investiguer GPT4o mini
https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/ 

voir comment utiliser les nouveaux modèles 4o et 4o mini avec les images par exemples. Faire tourner le code.

## SLM
small language models
--> cf video de Pamela



###########################################################
# API rates

https://help.openai.com/en/articles/6897202-ratelimiterror 

## organizations 
in https://platform.openai.com/account/org-settings
Ajouter des organisations selon le chat pour suivre les couts. Et pour éviter d'arriver à une limite d'usage de l'API
--> voir si possible avec AzureOpenAI


###########################################################
# moderations
Ajouter des seuils de modération spécifiques si nécessaires (différents de ceux définis par OpenAI) -> determine appropriate thresholds for each use case. 


###########################################################
# prompt engineering
Ecrire des prompts pour les différents use case
- content generation
- text transformation
- text classification
- in context learning : ajouter few shot prompting (ajouter des exemples)


###########################################################
# ajouter la possibilité de faire du speech to text
pour faire de la translation ou de la transcription ou les 2 à la fois. Voir si l'anglais est la seule langue (german to english but not german to french??) ou si pour la translation çà marche aussi en français ou en espagnol.
--> penser aux filiales espagnoles pour mieux communiquer avec elles. 


###########################################################
# fastAPI


###########################################################
# Langchain / llamaindex


###########################################################
# assistant API
assistant, threads, messages, runs
in beta version. not available in Azure Open AI
https://learn.microsoft.com/en-us/azure/ai-services/openai/assistants-reference?tabs=python 
