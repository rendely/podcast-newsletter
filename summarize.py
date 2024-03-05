from llm import LLM

CHAR_TO_TOKEN:float = 4.3  # approx based on sampling 92362 / 21340
# MAX_TOKENS:int = 16385  # for chat gpt 3.5 turbo
MAX_TOKENS:int = 1000  # for mistral ollama
SAFETY_FACTOR:float = 0.9  # have 20% safety factor on calculation
OVERLAP_FACTOR:float = 0.9
SPLIT_SIZE:int = round(CHAR_TO_TOKEN * MAX_TOKENS * SAFETY_FACTOR)


SUMMARIZE_PROMPT:str = '''You are an AI designed to summarize podcast transcript summaries. When a list of bullet points summarizing a podcast is provided, please organize it into topics, remove any duplicate bullets, but preserve all the information from the summaries to output a clean new final summary.'''

BULLET_PROMPT:str = '''You are an AI designed to summarize podcast transcripts with relevant extracts. When raw podcast transcripts are uploaded you will respond with a detailed 10 to 15 bullet point summary that preserves details of what was said, try to be more extractive instead of abstractive. If something sounds like it might be related to an ad, prepend #ad to that bullet.'''


class Summarizer:
    ''' Class for summarizing podcast transcripts'''

    def __init__(self, transcript: str, service:str):
        self.transcript: str = transcript
        self.transcript_chunks: list[str] = []
        self.create_chunks()
        self.summary_chunks: list[str] = []
        self.final_summary: str | None = None
        self.llm = LLM(service=service)

    def create_chunks(self):
        i = 0
        while i < len(self.transcript):
            section = self.transcript[i:i+SPLIT_SIZE]
            self.transcript_chunks.append(section)
            i += round(SPLIT_SIZE*OVERLAP_FACTOR)

    def summarize(self) -> str:
        if self.final_summary is not None:
            return self.final_summary

        print('Generating summary...')
        self.summarize_chunks()

        completion = self.llm.completion(
            SUMMARIZE_PROMPT,
            'Here is the podcast transcript summary bullet points:\n'
                 + '\n'.join(self.summary_chunks)
            )
        print(f'''Final summary:\n''')
        self.final_summary = completion
        print(f'''{self.final_summary}''')
        return self.final_summary

    def summarize_chunks(self):
        for chunk in self.transcript_chunks:
            print(f'''Summarizing chunk...''')
            self.summary_chunks.append(
                self.summarize_chunk(chunk)
            )

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
