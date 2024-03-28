from llm import LLM
import os
import json

CHAR_TO_TOKEN:float = 4.3  # approx based on sampling 92362 / 21340
# MAX_TOKENS:int = 16385  # for chat gpt 3.5 turbo
MAX_TOKENS:int = 2000  # for mistral ollama based on testing
SAFETY_FACTOR:float = 0.9  # have 20% safety factor on calculation
OVERLAP_FACTOR:float = 0.9
SPLIT_SIZE:int = round(CHAR_TO_TOKEN * MAX_TOKENS * SAFETY_FACTOR)


# SUMMARIZE_PROMPT:str = '''You are an AI designed to summarize podcast transcript summaries. When a list of bullet points summarizing a podcast is provided, please organize it into topics, remove any duplicate bullets, but preserve all the information from the summaries to output a clean new final summary.'''

SUMMARIZE_PROMPT:str = '''You are an AI designed to write email newsletters based on podcast transcripts. The user will provide you bullet points from a transcript of a podcast. Re-write this in prose preserving all the detail, in the voice of a concise, enthusiastic, business-savvy, hip, millenial author writing directly to the reader.'''

BULLET_PROMPT:str = '''You are an AI designed to summarize podcast transcripts with relevant extracts. When raw podcast transcripts are sent to you by the user you will respond with a detailed 10 bullet point summary that preserves details of what was said, try to be more extractive instead of abstractive.'''


class Summarizer:
    ''' Class for summarizing podcast transcripts'''

    def __init__(self, transcript: str, service:str, file_name:str|None):
        self.transcript: str = transcript
        self.transcript_chunks: list[str] = []
        self.create_chunks()
        self.summary_chunks: list[str] = []
        self.final_summary: str | None = None
        self.file_name: str = file_name
        self.llm = LLM(service=service)

    def create_chunks(self):
        i = 0
        while i < len(self.transcript):
            section = self.transcript[i:i+SPLIT_SIZE]
            self.transcript_chunks.append(section)
            i += round(SPLIT_SIZE*OVERLAP_FACTOR)

    def insights(self) -> str:
        self.summarize_chunks()
        print(f'''Extracting insights:\n\n''')

        completion = self.llm.completion(
            'You are an AI aimed at concisely extracting relevant insights',
                '\n'.join(self.summary_chunks) \
                + '\nExtract a list of all the key recommendations for listeners from this podcast transcript above'
            )
        print(completion)
        return completion

    def summarize(self) -> str:
        if self.final_summary is not None:
            return self.final_summary

        print('Generating summary...')
        self.summarize_chunks()
        print(f'''Creating final summary:\n\n''')

        completion = self.llm.completion(
            SUMMARIZE_PROMPT,
            'Here is the podcast transcript summary bullet points:\n'
                 + '\n'.join(self.summary_chunks)
            )
        
        self.final_summary = completion

        print(f'''{self.final_summary}''')
        
        with open(f'{self.file_name}-final-summary.txt', 'w') as f:
            f.write(self.final_summary)
        return self.final_summary

    def summarize_chunks(self):
        sum_chunks_file_name = f'{self.file_name}-sum-chunks.json'
        if sum_chunks_file_name in os.listdir():
            print('Loading from file')
            with open(sum_chunks_file_name, 'r') as f:
                self.summary_chunks = json.loads(f.read())
            return
        
        for i,chunk in enumerate(self.transcript_chunks):
            print(f'''Summarizing chunk {i+1} of {len(self.transcript_chunks)}...''')
            self.summary_chunks.append(
                self.summarize_chunk(chunk)
            )
        
        with open(sum_chunks_file_name, 'w') as f:
                f.write(json.dumps(self.summary_chunks, indent=4))

    def summarize_chunk(self, chunk: str) -> str:
        completion = self.llm.completion(
            BULLET_PROMPT,
            'Here is the podcast transcript:\n'
                 + chunk
            )
        print(f'''{completion}''')
        return completion

    def __repr__(self):
        return f'Summarizer(transcript={self.transcript[0:300]}...\n \
                 transcript_chunks={len(self.transcript_chunks)})'
