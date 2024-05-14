from ollama import chat, generate
import re

# def llmchat(prompt, model="llama3"):
#     response = chat(model=model, messages=[generate_message(prompt)])
#     return response['message']['content']

def generate_message(prompt):
    return {
        'role': 'user',
        'content': prompt,
        }

def llmchat(prompts, model="llama3"):
    messages = [generate_message(prompt) for prompt in prompts]
    response = chat(model=model, messages=messages)
    return response['message']['content']


def llmgenerate(prompt, model="llama3"):
    response = generate(model=model, prompt=prompt)
    return response['response']

def get_result(response):
    pattern = r"\|(.*?)\|(.*?)\|(.*?)\|"
    matches = re.findall(pattern, response)
    last_item = matches[2: -1]
    return last_item