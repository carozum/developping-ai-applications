# Working with the OpenAI API - Datacamp
1. Understand OpenAI API
2. Usage costs
3. Endpoints
4. parameters of the API requests
5. prompt engineering - to answer use cases
6. combining models - chaining
7. error handling (for production environment)
8. API rate




#################################################################
## 1. Understand OpenAI API
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

#################################################################
## 2. Usage costs
depending on the model requested and on the size of the model input and output
![cost calculation](image-7.png)
Calculating cost per time

#################################################################
## 3. endpoints : 

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
- storing responses to create a conversation history

### moderation endpoint
checks content for violations of the OPenai's usage policies, including : 
- incinting violence, 
- hate speech
- can customize model sensitivity to specific violations

The response consists in : 
- category violation : True/False
- category score : confidence of a violation. larger numbers --> greater certainty of violation. Numbers are between 0 and 1 but are not probabilities
- flagged True / False indicator of a violation

category scores : we have to determine appropriate thresholds for each use case. 
- stricter thresholds may result in *fewer false negative* (students communications in a school...). To flag more content even if that means accidentally flagging some non-violations. The goal is here to minimize the number of missed violations so called false negatives
- or more lenient thresholds may result in *fewer false positive* (communication, law enforcement) so reports on crimes are not accidentally flagged. Incorrectly flagging a crime report here would be an example of false positive. 

### audio endpoint : Speech to text transcription  with whisper
- model Whisper
- audio transcripts 
    - automating meeting transcripts
    - video caption generation (accessibility)
- translate audio from one language into an english transcript
- supports mp3, mp4, mpeg, mpga, m4a, wav, webm (25MB limit)
- other languages than english are supported

The audio file is read and then stored as binary format. 

### audio endpoint : Speech Translation with whisper
- Translate and transcribe audio
- limited to English transcripts? (german to english but not german to french ?)
- supports mp3, mp4, mpeg, mpga, m4a, wav, webm (25MB limit)
QUality varies on audio quality, audio language and model's knowledge. Beware before creating a whole application on that model and endpoint. --> to help the model do the best, we can provide a prompt to the model. Can improve the quality of the model by:
- providing an example of desired style
- provide context on transcript context



#################################################################
## 4. parameters of the API requests
- temperature : control on determinism, ranges from 0 (highly deterministic) to 2 (very random)
- max_tokens
- n number of responses
- model
- prompt
- topp
- frequencepenalty

### response_format parameter for the API
- response format both in the prompt and as a parameter.
- what are the other formats? Json is very used and useful



#################################################################
## 5. prompt engineering - to answer use cases

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
*few shot prompting* a handful of examples provided



#################################################################
## 6. combining models - chaining

![combining chaining models](image-9.png)
*chaining* :feeding output from one model into another model.
- summarizing a meeting recording chaining whisper to gpt text model



#################################################################
## 7. error handling (for production environment)

AI systems are complex so 
- simplifying the user experience is crucial. 
- eliminating barriers to using these system
- display a user friendly error message 
- alternatives for when the service is unavailable

*Connection errors* : 
Generally due to connection issues on either the user's or the service's side. 
--> InternalServerError, APIConnectionError, APITimeoutError
--> solution : check our connection configuration (firewalls), wait and retry. Reach out the support if that fails. 

*Resource Limits Errors *
Generally due limits on the frequency of requests or the amount of text passed.
--> RateLimitError, ConflictError
--> solution : ensure that the requests are paced within the limits of the API : reducing the amount of text in the requests sent or staggering requests if they are frequent 

*Authentication Errors*
AuthenticationError code 401, Incorrect API key

*Bad request Errors*
The request  was malformed or missing some required parameters (invalid messages...) or model deprecated : NotFoundError code 404

==> try except blocks to encapsulate the API call !



#################################################################
## 8. API rate

API rate limits are another key consideration for companies building features on the OpenAI API. Rate limits are a cap on the frequency and size of API requests. They are put in place to ensure fair access to the API, prevent misuse, and also manage the infrastructure that supports the API. For many cases, this may not be an issue, but if a feature is exposed to a large user base, or the requests require generating large bodies of content, they could be at risk of hitting the rate limits. https://platform.openai.com/docs/guides/rate-limits

If you send many requests or use lots of tokens in a short period, you may hit your rate limit and see an ```openai.error.RateLimitError```. If you see this error, please wait a minute for your quota to reset and you should be able to begin sending more requests. Please see OpenAI's rate limit error support article for more information. https://help.openai.com/en/articles/6897202-ratelimiterror

What are the solutions to the rate limit errors ? Handling this error will help us maximize the requests to the API while minimizing delays and avoiding failed responses. Rate limits regulate the flow of data between users and the API. By avoiding single users from making excessive requests, rate limits can prevent malicious attacks, as well as ensuring a balanced distribution between users within an organization.

Much of this risk can be mitigated by, instead of running multiple features under the same organization.


### First solution to API rates : organizations
For business use cases with frequent requests to the API, it's important to manage usage across the business. Setting up an organization for the API allows for better management of access, billing, and usage limits to the API. Users can be part of multiple organizations and attribute requests to specific organizations for billing. https://platform.openai.com/account/org-settings

To attribute a request to a specific organization, we only need to add one more line of code. Like the API key, the organization ID can be set before the request.

#### Organization structure

having separate organizations for each business unit or product feature, depending on the number of features built on the OpenAI API.

![organisation structure](image-6.png)

In this example, we've created separate OpenAI organizations for three different AI-powered features: a customer service chatbot, a content recommendation system, and a video transcript generator. This distributes the requests to reduce the risk of hitting the rate limit. It also removes the single failure point, so an issue to one organization, such as a billing issue, will only result in the failure of a single feature. Product-separated organizations also provides more granular insights into usage and billing.

you can set up organizations to manage API usage and billing. Users can be part of multiple organizations and attribute API requests to a specific organization. It's best practice to structure organizations such that each business unit or product feature has a separate organization, depending on the number of features the business has built on the OpenAI API.


### Second solution : limit the number of tokens 
In the parameters of the request


### Third solution : 



#################################################################
## 9. moderation and safety
- control unwanted inputs
- minimizing the risk of data leaks

#################################################################
## 10. testing and validation
- checking for responses that are out of topic
- testing for inconsistent behavior

#################################################################
## 11. communication with external systems
- calling external functions and APIs
- Optimizing response times


#################################################################
## Annexes
converting the response into a dictionary
print(response.model_dump())