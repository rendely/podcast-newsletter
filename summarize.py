from openai import OpenAI
import os 

CHAR_TO_TOKEN = 4.3 # approx based on sampling 92362 / 21340
MAX_TOKENS = 16385 #for chat gpt 3.5 turbo
SAFETY_FACTOR = 0.8 #have 20% safety factor on calculation
SPLIT_SIZE = round(CHAR_TO_TOKEN * MAX_TOKENS * SAFETY_FACTOR)
MODEL = "gpt-3.5-turbo"


client = OpenAI(
   api_key=os.environ.get("OPEN_API_KEY"),
 )

class Summarizer:
    ''' Class for summarizing podcast transcripts'''
    def __init__(self, transcript: str):
        self.transcript: str = transcript
        self.transcript_chunks: list[str] = ['']
        self.summary_chunks: list[str] = []
        self.final_summary: str|None = None
        for section in transcript.split(' '):
            if len(section)+len(self.transcript_chunks[-1]) < SPLIT_SIZE:
                self.transcript_chunks[-1] += section + ' '
            else:
                self.transcript_chunks.append(section+ ' ')        

    def summarize(self):
        if self.final_summary is not None:
            return self.final_summary
        
        print('Generating summary...')
        self.summarize_chunks()

        completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI designed to summarize podcast transcript summaries. When a list of bullet points summarizing a podcast is provided, please organize it into topics, remove any duplicate bullets, but preserve all the information from the summaries to output a clean new final summary."},
            {"role": "user", "content": 'Here is the podcast transcript summary bullet points:\n' \
             + '\n'.join(self.summary_chunks)}
        ]
        )
        print('Final summary:\n')
        self.final_summary = completion.choices[0].message.content
        print('self.final_summary')
        return self.final_summary
    
    def summarize_chunks(self):        
        for chunk in self.transcript_chunks:
            print(f'Summarizing chunk...')
            self.summary_chunks.append(
                self.summarize_chunk(chunk)
                )
            
    def summarize_chunk(self, chunk:str)-> str:        
        completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI designed to summarize podcast transcripts. When raw podcast transcripts are uploaded you will respond with a detailed 10 to 15 bullet point summary that preserves details of what was said. If something sounds like it might be related to an ad, prepend #ad to that bullet."},
            {"role": "user", "content": 'Here is the podcast transcript:\n' \
             + chunk}
        ]
        )
        return completion.choices[0].message.content
        
    def __repr__(self):
        return f'Summarizer(transcript={self.transcript[0:300]}...\n \
                 transcript_chunks={len(self.transcript_chunks)})'