from openai import OpenAI
import ollama
import anthropic
import os

OPENAI_MODEL:str = 'gpt-4-turbo-preview'
OLLAMA_MODEL:str = 'mistral:latest'
ANTHROPIC_MODEL:str = 'claude-3-opus-20240229'

openai_client = OpenAI(
    api_key=os.environ.get("OPEN_API_KEY"),
)

anthropic_client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)


class LLM:
    '''Class for getting LLM completions with different services'''
    def __init__(self, service:str='openai'):
        print(f'''Using {service} for LLM''')
        self.service = service

    def completion(self, sys_prompt:str, user_prompt:str) -> str:
        if self.service == 'ollama':
            completion = ollama.chat(
                model=OLLAMA_MODEL, 
                messages=[
                    {'role': 'system', "content": sys_prompt},
                    {'role': 'user', "content": user_prompt},
                    ]
                )
            return completion['message']['content']
            
        if self.service == 'openai':
            completion = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                    ]
                )
            print(completion.usage)
            return completion.choices[0].message.content
    
        if self.service == 'anthropic':
            completion = anthropic_client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=4096, #max
                system=sys_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                    ]
                )
            print(completion.usage)
            return completion.content[0].text
    
        raise ValueError('Must select a supported service')
    
    def __repr__(self):
        return f'LLM<service={self.service}>'