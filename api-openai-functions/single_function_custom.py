##############################################################
# use case 2 : applied a custom function
# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling

from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI
import json
from zoneinfo import ZoneInfo
from datetime import datetime

_ = load_dotenv((find_dotenv()))
openai_api_key = os.environ["OPENAI_API_KEY"]

model = "gpt-4o"

# Set your API key
client = OpenAI(api_key=openai_api_key)


####################################################
# define the function


# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}


def get_current_time(location):
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")
    location_lower = location.lower()

    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")
            current_time = datetime.now(
                ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })

    print(f"No timezone data found for {location_lower}")
    return json.dumps({"location": location, "current_time": "unknown"})


######################################################
# run conversation


# Initial user message
# Single function call
messages1 = [
    {"role": "user", "content": "What's the current time in San Francisco"}]
messages2 = [
    {"role": "user", "content": "What's generative AI?"}]
# messages = [{"role": "user", "content": "What's the current time in San Francisco, Tokyo, and Paris?"}] # Parallel function call with a single tool/function defined


def run_conversation(messages):

    # Define the function for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the function
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")
    print(response_message)

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "get_current_time":
                function_args = json.loads(tool_call.function.arguments)
                print(f"Function arguments: {function_args}")
                time_response = get_current_time(
                    location=function_args.get("location")
                )
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_current_time",
                    "content": time_response,
                })
    else:
        print("No tool calls were made by the model.")

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return final_response.choices[0].message.content


###################################################################
# conversation using tool_calls
# Run the conversation and print the result
print(run_conversation(messages1))


"""Model's response:
ChatCompletionMessage(content=None, refusal=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_p74gJw1LIVAaoQuZXKH9TRAJ', function=Function(arguments='{"location":"San Francisco"}', name='get_current_time'), type='function')])
Function arguments: {'location': 'San Francisco'}
get_current_time called with location: San Francisco
Timezone found for san francisco
The current time in San Francisco is 5:23 AM.
    """

##################################################################
# conversation without tool_calls

print(run_conversation(messages2))

"""Model's response:
ChatCompletionMessage(content='Generative AI refers to a category of artificial intelligence systems designed to generate new content. This can include text, images, music, videos, or even code. These systems use large datasets and sophisticated algorithms to learn patterns and structures within the data they are trained on, which allows them to create original content that mimics the properties of the input data.\n\nHere are some key aspects of generative AI:\n\n1. **Machine Learning Models**: Generative AI typically relies on advanced machine learning models such as Generative Adversarial Networks (GANs), Variational Autoencoders (VAEs), and Transformers. These models are trained to understand and replicate data patterns.\n\n2. **Applications**:\n   - **Text Generation**: Tools like GPT-3 (OpenAI) can generate human-like text for various purposes, such as writing articles, answering questions, or creating conversational agents.\n   - **Image Generation**: GANs can create realistic images, which can be used in art, design, or even deepfake technology.\n   - **Music and Audio**: AI can compose music or generate sounds that mimic existing musical styles.\n   - **Code Generation**: AI can help write code snippets or even entire applications based on user inputs and requirements.\n\n3. **Creativity and Innovation**: Generative AI augments human creativity by providing new ways to create and innovate. It can act as a tool to inspire new ideas, automate repetitive creative tasks, or explore design spaces that might be too complex for humans to tackle alone.\n\n4. **Challenges**: Despite its potential, generative AI also raises ethical and practical challenges, including issues related to copyright infringement, the creation of misleading or harmful content, and the computational resources required for training large models.\n\nOverall, generative AI represents a significant advancement in artificial intelligence, with the potential to transform various industries by automating and enhancing creative processes.', refusal=None, role='assistant', function_call=None, tool_calls=None)

No tool calls were made by the model.

Generative AI is a branch of artificial intelligence focused on creating new content, such as text, images, music, and more. Rather than just analyzing data or performing predefined tasks, generative AI systems can produce original and often highly sophisticated content by learning patterns and structures from massive datasets. Here's a deeper look into some of the key concepts and components:

### Key Concepts:

1. **Machine Learning Models**:
   - **Generative Adversarial Networks (GANs)**: Consist of two neural networks, a generator and a discriminator, that work against each other to produce increasingly realistic samples.
   - **Variational Autoencoders (VAEs)**: Learn to encode data into a latent space and then decode it back, allowing for the generation of new samples.
   - **Transformers**: Used prominently in natural language processing (NLP); models like GPT (Generative Pre-trained Transformer) have gained attention for their ability to generate coherent and contextually relevant text.

2. **Training on Large Datasets**: Generative models require vast amounts of data to learn the statistical properties of the target content. This data helps the model understand the nuances and variability required for generating new, high-quality output.

### Applications:

1. **Text Generation**:
   - **Chatbots and Virtual Assistants**: Platforms like OpenAI's GPT-3 can converse in natural language, providing human-like responses.
   - **Content Creation**: Automated writing for articles, reports, and creative stories.

2. **Image Generation**:
   - **Art and Design**: Creating new artworks or design elements.
   - **Fashion**: Generating new clothing designs.
   - **Deepfakes**: Creating highly realistic images or videos of people that do not exist.

3. **Music and Audio**:
   - **Composition**: AI can create new musical pieces or soundtracks.
   - **Audio Synthesis**: Generating new sounds or enhancing existing audio.

4. **Code Generation**:
   - **Coding Assistants**: Tools like GitHub Copilot assist developers by suggesting code snippets or even generating entire functions.

### Benefits:

1. **Creativity and Innovation**: Generative AI can help human creators by providing inspiration or automating repetitive tasks, enabling them to focus on higher-level creative processes.
2. **Efficiency**: Automates the generation of content, saving time and effort compared to manual creation.
3. **Personalization**: Can create customized content tailored to individual preferences or needs.

### Challenges:

1. **Ethical Issues**: Concerns about the misuse of generated content, such as deepfakes or misleading information.
2. **Intellectual Property**: Questions around copyright and the ownership of AI-generated content.
3. **Resource-Intensive**: Training generative models often requires significant computational power and energy.
4. **Quality Control**: Ensuring the generated content is accurate, appropriate, and high quality can be difficult.

### Emerging Trends:

1. **Hybrid Models**: Combining generative AI with other AI disciplines to enhance capabilities.
2. **Real-Time Generation**: Improvements in computational power and algorithms are making real-time generative applications more feasible.
3. **Ethical AI**: Development of frameworks and guidelines to ensure responsible use of generative technologies.

Generative AI is rapidly evolving and holds immense potential across various fields, transforming how we create, interact with, and consume digital content."""
