# Working with the OpenAI API - Datacamp
https://platform.openai.com/signup 
https://platform.openai.com/account/api-keys 

![openai context](image.png)


![What is API?](image-2.png)
API Application programming interface : act as messengers between software applications, taking a request to a system and receiving a response containing data or services


![The OpenAI API](image-4.png)
We can write code to interact with the OpenAI API and request the use of one of their models


Open AI has its own python library called openai, an abstraction to make requests to the API, importing the OpenAI Class from openai library which is used to instantiate a python API client. The client configures the environment for communicating with the API and make the request 

the OpenAI endpoints (see openAI documentation): 
- Authentication key

### Usage costs
depending on the model requested and on the size of the model input and output
![cost calculation](image-7.png)
Calculating cost per time

## endpoints : 
![the endpoints](image-5.png)
![completions and chat completions](image-8.png)

### completions endpoint (single turn) : 
Usually using a *gpt35-turbo-instruct* to perform single turn
- used with a prompt (input text)
- generate text (output text) to complete the prompt in a likely and consistent way
- the response is a Completion object with various attributes
- tasks : answer questions, classification into categories, sentiment analysis, explaining complex topics

### chat endpoint (multiturn tasks)
usually using a *gpt35-turbo* to perform multi turn : cheaper that the turbo instruct. 
ideation, customer support assistant, personal tutor, translating languages, writing code... or perform single turn tasks. 
- existence of roles for better customization :system (behavior of the assistant), user (instruct the assistant), assistant (response to the user instruction). 
- The assistant role can also be written by the user to provide examples to help the model better understand.
- the prompt is now a list of messages, each message being a dictionary with a role

### moderation endpoint
checks content for violations of the OPenai's usage policies, including : 
- incinting violence, 
- hate speech
- can customize model sensitivity to specific violations


## converting the response into a dictionary
print(response.model_dump())


## organisations
For business use cases with frequent requests to the API, it's important to manage usage across the business. Setting up an organization for the API allows for better management of access, billing, and usage limits to the API. Users can be part of multiple organizations and attribute requests to specific organizations for billing.

https://platform.openai.com/account/org-settings

To attribute a request to a specific organization, we only need to add one more line of code. Like the API key, the organization ID can be set before the request.

## API rate
API rate limits are another key consideration for companies building features on the OpenAI API. Rate limits are a cap on the frequency and size of API requests. They are put in place to ensure fair access to the API, prevent misuse, and also manage the infrastructure that supports the API. For many cases, this may not be an issue, but if a feature is exposed to a large user base, or the requests require generating large bodies of content, they could be at risk of hitting the rate limits.

https://platform.openai.com/docs/guides/rate-limits

If you send many requests or use lots of tokens in a short period, you may hit your rate limit and see an ```openai.error.RateLimitError```. If you see this error, please wait a minute for your quota to reset and you should be able to begin sending more requests. Please see OpenAI's rate limit error support article for more information.
https://help.openai.com/en/articles/6897202-ratelimiterror

Much of this risk can be mitigated by, instead of running multiple features under the same organization,

## Organization structure

having separate organizations for each business unit or product feature, depending on the number of features built on the OpenAI API.

![organisation structure](image-6.png)

In this example, we've created separate OpenAI organizations for three different AI-powered features: a customer service chatbot, a content recommendation system, and a video transcript generator. This distributes the requests to reduce the risk of hitting the rate limit. It also removes the single failure point, so an issue to one organization, such as a billing issue, will only result in the failure of a single feature. Product-separated organizations also provides more granular insights into usage and billing.

you can set up organizations to manage API usage and billing. Users can be part of multiple organizations and attribute API requests to a specific organization. It's best practice to structure organizations such that each business unit or product feature has a separate organization, depending on the number of features the business has built on the OpenAI API.


## parameters
- temperature : control on determinism, ranges from 0 (highly deterministic) to 2 (very random)
- max_tokens
- n number of responses
- model
- prompt
- topp
- frequencepenalty



## use cases - prompt engineering - completions / chat completions endpoints
Providing a more specific prompt gave you much greater control over the model's response
- content generation : 
    - question answering
    - ideation """create a tagline for a new hotdog stand"""
    
- content transformation (changing based on an instruction)
    - Find and replace : temperature 0.5, max_tokens 100
    - summarization : temperature 0, max_tokens 400
    - copyediting
    Begin with the instruction and then the text to transform. 
    """Update name to Maarten, pronouns to he/him and job title to Senior Content Developer in:
    Joanne is an AI developer. She likes playing with her kids"""

- text classification : assigning a label to a piece of information
    - identifying the language from text
    - categorization (sorting places)
    - classifying sentiments
Completions endpoint can perform these tasks providing the model has sufficient knowledge and the prompt contains sufficient context.

*zero shot prompting* no example provided

*In context-learning*
*one shot prompting* one example provided
*few shot prompting* a handful of examples provides