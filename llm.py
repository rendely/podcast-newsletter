from openai import OpenAI
import os

MODEL = "gpt-3.5-turbo"

client = OpenAI(
    api_key=os.environ.get("OPEN_API_KEY"),
)


class LLM:
    '''Class for getting LLM completions with different services'''
    def __init__(self, service:str='openai'):
        self.service = service

    def completion(self, sys_prompt, user_prompt):
        if self.service == 'openai':
            completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
            print(completion.usage)
            return completion.choices[0].message.content
    
    def __repr__(self):
        return f'LLM<service={self.service}>'